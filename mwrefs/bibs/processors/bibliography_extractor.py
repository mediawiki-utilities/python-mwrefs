import collections
import functools
import datetime

import more_itertools
import fuzzywuzzy.process

from .. import utils, extractors, dumper, languages

FUZZY_MATCH_CUTOFF = 91      # between 0, 100

features_template = '''
<%!
    from itertools import groupby
    def groupby_action(diff):
        return groupby(diff, lambda d: d.action)
%>
<%def name="attribute_if_exists(name, text)" filter="trim">
    % if text is not None:
        ${name}="${text | x}"
    % endif
</%def>
<%def name="tag_user_if_exists(user)" filter="trim">
    % if user:
        <user ${attribute_if_exists('id', user.id)} ${attribute_if_exists('name', user.text)} />
    % endif
</%def>
<root>
    % for page in pages:
    <page>
        <title>${page.title | x}</title>
        <id>${page.id | x}</id>
        <revisions>
            % for revision in page.revisions:
            <revision>
                <id>${revision.id | x}</id>
                ${tag_user_if_exists(revision.user)}
                <timestamp>${revision.timestamp | x}</timestamp>
                <sections>
                    % for section in revision.sections:
                        <section name="${section.name | x}" level="${section.level | x}">${section.body | x}</section>
                    % endfor
                </sections>
            </revision>
            % endfor
        </revisions>
    </page>
    % endfor
</root>
'''

stats_template = '''
<stats>
    <performance>
        <start_time>${stats['performance']['start_time'] | x}</start_time>
        <end_time>${stats['performance']['end_time'] | x}</end_time>
        <revisions_analyzed>${stats['performance']['revisions_analyzed'] | x}</revisions_analyzed>
        <pages_analyzed>${stats['performance']['pages_analyzed'] | x}</pages_analyzed>
    </performance>
    <extracted-section-names>
        % for key in ['global', 'last_revision']:
        <${key}>
            % for section_name, count in stats['section_names'][key].most_common():
            <section name="${section_name | x}" count="${count}" />
            % endfor
        </${key}>
        % endfor
    </extracted-section-names>
</stats>
'''

Page = collections.namedtuple('Page', [
    'id',
    'title',
    'revisions',
])
Revision = collections.namedtuple('Revision', [
    'id',
    'user',
    'timestamp',
    'sections',
])


# TODO: instead of comparing section_name to a bib synonym,
# search all the possible bib synonyms in the section name
@functools.lru_cache(maxsize=500)
def is_secion_bibliography(section_name, language, score_cutoff=FUZZY_MATCH_CUTOFF):
    bibliography_synonyms = languages.bibliography[language]
    match = fuzzywuzzy.process.extractOne(
        section_name,
        bibliography_synonyms,
        score_cutoff=score_cutoff,
    )
    return bool(match)


def extract_revisions(mw_page, language, stats, only_last_revision):
    section_names_stats = stats['section_names']
    revisions = more_itertools.peekable(mw_page)
    for mw_revision in revisions:
        utils.dot()

        is_last_revision = not utils.has_next(revisions)
        if only_last_revision and not is_last_revision:
            continue

        text = utils.remove_comments(mw_revision.text or '')

        sections = (section for section, _ in extractors.sections(text))

        bibliography_sections = list(section
            for section in sections
            if is_secion_bibliography(section.name, language))

        for section in bibliography_sections:
            section_names_stats['global'][section.name] += 1
            if is_last_revision:
                section_names_stats['last_revision'][section.name] += 1

        yield Revision(
            id=mw_revision.id,
            user=mw_revision.user,
            timestamp=mw_revision.timestamp.to_json(),
            sections=bibliography_sections,
        )

        stats['performance']['revisions_analyzed'] += 1


def extract_pages(dump, language, stats, only_last_revision):
    for mw_page in dump:
        utils.log("Processing", mw_page.title)

        # Skip non-articles
        if mw_page.namespace != 0:
            utils.log('Skipped (namespace != 0)')
            continue

        revisions_generator = extract_revisions(
            mw_page,
            language=language,
            stats=stats,
            only_last_revision=only_last_revision,
        )

        yield Page(
            id=mw_page.id,
            title=mw_page.title,
            revisions=revisions_generator,
        )
        stats['performance']['pages_analyzed'] += 1


def configure_subparsers(subparsers):
    parser = subparsers.add_parser('extract-bibliography',
        help='Extract only sections may be a bibliography')
    parser.add_argument('-l', '--language',
        choices=languages.supported,
        required=True,
        help='The language of the dump.',
    )
    parser.add_argument('--only-last-revision',
        action='store_true',
        help='Consider only the last revision for each page.',
    )
    parser.set_defaults(func=main)


def main(dump, features_output_h, stats_output_h, args):
    stats = {
        'performance': {
            'start_time': None,
            'end_time': None,
            'revisions_analyzed': 0,
            'pages_analyzed': 0,
        },
        'section_names': {
            'global': collections.Counter(),
            'last_revision': collections.Counter(),
        },
    }
    pages_generator = extract_pages(dump,
        language=args.language,
        stats=stats,
        only_last_revision=args.only_last_revision,
    )
    with features_output_h:
        stats['performance']['start_time'] = datetime.datetime.utcnow()
        dumper.render_template(
            features_template,
            output_handler=features_output_h,
            pages=pages_generator,
        )
        stats['performance']['end_time'] = datetime.datetime.utcnow()

    with stats_output_h:
        dumper.render_template(
            stats_template,
            stats_output_h,
            stats=stats,
        )
