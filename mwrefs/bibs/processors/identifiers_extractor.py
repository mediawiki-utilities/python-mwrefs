import collections
import datetime
import more_itertools

from .. import utils, extractors, dumper

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
                <publication-identifiers-diff>
                    % for key, group in groupby_action(revision.publication_identifiers_diff):
                    <diff action="${key | x}">
                        % for _, identifier in group:
                        <identifier type="${identifier.type | x}" id="${identifier.id | x}" />
                        % endfor
                    </diff>
                    % endfor
                </publication-identifiers-diff>
            </revision>
            %endfor
        </revisions>
    </page>
    % endfor
</root>
'''

stats_template = '''
<stats>
    <performance>
        <start_time>${stats['performance']['start_time']}</start_time>
        <end_time>${stats['performance']['end_time']}</end_time>
        <revisions_analyzed>${stats['performance']['revisions_analyzed']}</revisions_analyzed>
        <pages_analyzed>${stats['performance']['pages_analyzed']}</pages_analyzed>
    </performance>
    <identifiers>
        % for key in ['global', 'last_revision']:
        <${key}>
            % for where, count in stats['identifiers'][key].items():
            <appearance where="${where}" count="${count}" />
            % endfor
        </${key}>
        % endfor
    </identifiers>
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
    'publication_identifiers_diff',
])

def IdentifierStatsDict():
    return {
        'only_in_raw_text': 0,
        'only_in_tag_ref': 0,
        'only_in_template': 0,
        'in_tag_ref_and_template': 0,
    }


@utils.listify(wrapper=set)
def where_appears(span, **spans):
    span_le = extractors.Span.__le__
    for key, span_list in spans.items():
        # if any(span <= other_span) for other_span in span_list):
        # HACK: the following is more efficient. Sorry :(
        if any(span_le(span, other_span) for other_span in span_list):
            yield key


def identifier_appearance_stat_key(appearances):
    if {'templates', 'references'} <= appearances:
        return 'in_tag_ref_and_template'
    elif 'templates' in appearances:
        return 'only_in_template'
    elif 'references' in appearances:
        return 'only_in_tag_ref'
    else:
        return 'only_in_raw_text'


def extract_revisions(page, stats, only_last_revision):
    revisions = more_itertools.peekable(page)

    prev_identifiers = set()
    for mw_revision in revisions:
        utils.dot()

        is_last_revision = not utils.has_next(revisions)
        if only_last_revision and not is_last_revision:
            continue

        text = utils.remove_comments(mw_revision.text or '')

        references_captures = list(extractors.references(text))

        templates_captures = list(extractors.templates(text))

        identifiers_captures = list(extractors.pub_identifiers(text))
        identifiers = [identifier for identifier, _ in identifiers_captures]

        for identifier, span in identifiers_captures:
            appearances = where_appears(span,
                references=(span for _, span in references_captures),
                templates=(span for _, span in templates_captures),
            )
            key_to_increment = identifier_appearance_stat_key(appearances)

            stats['identifiers']['global'][key_to_increment] += 1
            if is_last_revision:
                stats['identifiers']['last_revision'][key_to_increment] += 1

        yield Revision(
            id=mw_revision.id,
            user=mw_revision.user,
            timestamp=mw_revision.timestamp.to_json(),
            publication_identifiers_diff=utils.diff(prev_identifiers,
                                              identifiers),
        )

        stats['performance']['revisions_analyzed'] += 1
        prev_identifiers = identifiers


def extract_pages(dump, stats, only_last_revision):
    for mw_page in dump:
        utils.log("Processing", mw_page.title)

        # Skip non-articles
        if mw_page.namespace != 0:
            utils.log('Skipped (namespace != 0)')
            continue

        revisions_generator = extract_revisions(
            mw_page,
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
    parser = subparsers.add_parser('extract-identifiers',
        help='Extract the identifiers from the text (doi, isbn, arxiv and pubmed.')
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
        'identifiers': {
            'global': IdentifierStatsDict(),
            'last_revision': IdentifierStatsDict(),
        },
    }
    pages_generator = extract_pages(dump,
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
