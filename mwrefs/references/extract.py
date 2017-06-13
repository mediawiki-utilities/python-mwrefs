import re
from collections import defaultdict
from itertools import chain

import mwparserfromhell
from mwcites.extractors import arxiv, doi, isbn, pubmed

LEXEME = [
    ('ref_singleton', re.compile(r'<ref(\s[^/>]*)?/>', re.M | re.I)),
    ('ref_tag', re.compile(r'<ref(\s[^/>]*)?>[\s\S]*?</ref>', re.M | re.I)),
    ('header', re.compile(
        r'(\n|^)(=[^=]+=|==[^=]+==|===[^=]+===|====[^=]+====|' +
        r'=====[^=]+=====|======[^=]+======)', re.M | re.I))]

GROUP_RE = re.compile('|'.join('(?P<{0}>{1})'.format(name, regex.pattern)
                               for name, regex in LEXEME), re.M | re.I)

PLAIN_PROTO = [r'bitcoin', r'geo', r'magnet', r'mailto', r'news', r'sips?',
               r'tel', r'urn']
SLASHED_PROTO = [r'', r'ftp', r'ftps', r'git', r'gopher', r'https?', r'ircs?',
                 r'mms', r'nntp', r'redis', r'sftp', r'ssh', r'svn', r'telnet',
                 r'worldwind', r'xmpp']
ADDRESS = r'[^\s/$.?#<>].[^\s<>]*'

URL_RE = re.compile(
    r'(' +  # noqa
        r'(' + '|'.join(PLAIN_PROTO) + r')\:|' +  # noqa
        r'((' + '|'.join(SLASHED_PROTO) + r')\:)?\/\/' +
    r')' + ADDRESS, re.I | re.M)
# re.compile(url, re.U).match("https://website.gov?param=value")


def extract(content):
    current_section = 0
    last_header, last_level_2 = None, None
    named_occurrences = defaultdict(list)
    references = []

    for match in GROUP_RE.finditer(content):
        if match.lastgroup == 'header':
            level = header_level(match)
            if level == 2:
                last_level_2 = match
            last_header = match
            current_section += 1
        else:
            ref_tag = mwparserfromhell.parse(match.group(0)).filter_tags()[0]
            name = (str(ref_tag.get('name').value)
                    if ref_tag.has('name') else None)
            if name is not None:
                named_occurrences[name].append(
                    (match, current_section, last_header, last_level_2))
            else:
                reference_doc = build_reference(name, match)
                occurrence_doc = build_occurrence(
                    content, match, current_section, last_header, last_level_2)
                reference_doc['occurrences'].append(occurrence_doc)
                references.append(reference_doc)

    for name, occurrences in named_occurrences.items():
        ref_tags = [oc for oc in occurrences if oc[0].lastgroup == "ref_tag"]
        if len(ref_tags) > 0:
            reference_doc = build_reference(name, ref_tags[0][0])
        else:
            reference_doc = build_reference(name, occurrences[0][0])

        reference_doc['occurrences'] = [
            build_occurrence(content, m, s, lh, ll2)
            for m, s, lh, ll2 in occurrences]
        references.append(reference_doc)

    def get_offset(rd):
        return rd['occurrences'][0]['text_offset']

    for reference_doc in sorted(references, key=get_offset):
        yield reference_doc


def header_level(match):
    equals = 0
    if match is not None:
        for character in match.group(0).strip("\n"):
            if character == "=":
                equals += 1
            else:
                break

    return equals


def build_reference(name, match):
    # Extract reference content
    wikicode = mwparserfromhell.parse(match.group(0))
    templates = wikicode.filter_templates()
    return {
        'name': name,
        'raw_content': match.group(0),
        'templated': len(templates) > 0,
        'cite_template': (str(templates[0].name)
                          if len(templates) > 0 else None),
        'urls': [m.group(0) for m in URL_RE.finditer(match.group(0))],
        'identifiers': list(chain(*(ext.extract(match.group(0))
                                    for ext in (doi, pubmed, arxiv, isbn)))),
        'occurrences': []
    }


def build_occurrence(content, match, current_section, last_header,
                     last_level_2):
    start_offset, end_offset = match.span()
    return {
        'section': current_section,
        'text_offset': start_offset,
        'preceding_text': content[max(0, start_offset - 250):start_offset],
        'succeeding_text': content[
            end_offset:min(len(content), end_offset + 250)],
        'header_level': header_level(last_header),
        'header_text': (last_header.group(0).strip(" =\n")
                        if last_header is not None else None),
        'header_offset': (last_header.start()
                          if last_header is not None else None),
        'level_2_text': (last_level_2.group(0).strip(" =\n")
                         if last_level_2 is not None else None),
        'level_2_offset': (last_level_2.start()
                           if last_level_2 is not None else None)
    }
