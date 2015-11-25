import collections
import datetime

import more_itertools

from .. import utils, extractors, dumper


stats_template = '''
<stats>
    <performance>
        <start_time>${stats['performance']['start_time']}</start_time>
        <end_time>${stats['performance']['end_time']}</end_time>
        <revisions_analyzed>${stats['performance']['revisions_analyzed']}</revisions_analyzed>
        <pages_analyzed>${stats['performance']['pages_analyzed']}</pages_analyzed>
    </performance>
    <section-names-per-revision>
        % for key in ['global', 'last_revision']:
        <${key}>
            % for section_name, count in stats['section_names_per_revision'][key].most_common():
            <section name="${section_name | x}" count="${count}" />
            % endfor
        </${key}>
        % endfor
    </section-names-per-revision>
    <sections-per-revision>
        % for key in ['global', 'last_revision']:
        <${key}>
            % for sections_in_revision, count in stats['sections_per_revision'][key].most_common():
            <sections number="${sections_in_revision}" count="${count}" />
            % endfor
        </${key}>
        % endfor
    </sections-per-revision>
    <revisions>
        <global count="${stats['revisions']['global']}" />
        <last_revision count="${stats['revisions']['last_revision']}" />
    </revisions>
</stats>
'''


def analyze_revisions(page, stats, only_last_revision):
    revisions = more_itertools.peekable(page)

    section_names_stats = stats['section_names_per_revision']
    sections_stats = stats['sections_per_revision']

    for mw_revision in revisions:
        utils.dot()

        is_last_revision = not utils.has_next(revisions)
        if only_last_revision and not is_last_revision:
            continue

        text = utils.remove_comments(mw_revision.text or '')

        section_names = [section.name.strip().lower()
                         for section, _ in extractors.sections(text)]
        sections_count = len(section_names)

        for section_name in section_names:
            section_names_stats['global'][section_name] += 1
            if is_last_revision:
                section_names_stats['last_revision'][section_name] += 1

        sections_stats['global'][sections_count] += 1
        if is_last_revision:
            sections_stats['last_revision'][sections_count] += 1

        stats['revisions']['global'] += 1
        if is_last_revision:
            stats['revisions']['last_revision'] += 1

        stats['performance']['revisions_analyzed'] += 1


def analyze_pages(dump, stats, only_last_revision):
    for mw_page in dump:
        utils.log("Processing", mw_page.title)

        # Skip non-articles
        if mw_page.namespace != 0:
            utils.log('Skipped (namespace != 0)')
            continue

        analyze_revisions(
            mw_page,
            stats=stats,
            only_last_revision=only_last_revision,
        )

        stats['performance']['pages_analyzed'] += 1


def configure_subparsers(subparsers):
    parser = subparsers.add_parser('count-sections',
        help='Count the number of sections and the section names of the dump.')
    parser.add_argument('--only-last-revision',
        action='store_true',
        help='Consider only the last revision for each page.',
    )
    parser.set_defaults(func=main)


def main(dump, features_output_h, stats_output_h, args):
    stats = {
        'sections_per_revision': {
            'global': collections.Counter(),
            'last_revision': collections.Counter(),
        },
        'section_names_per_revision': {
            'global': collections.Counter(),
            'last_revision': collections.Counter(),
        },
        'revisions': collections.Counter(),
        'performance': {
            'start_time': None,
            'end_time': None,
            'revisions_analyzed': 0,
            'pages_analyzed': 0,
        }
    }
    stats['performance']['start_time'] = datetime.datetime.utcnow()
    analyze_pages(dump,
        stats=stats,
        only_last_revision=args.only_last_revision,
    )
    stats['performance']['end_time'] = datetime.datetime.utcnow()

    with stats_output_h:
        dumper.render_template(
            stats_template,
            stats_output_h,
            stats=stats,
        )
