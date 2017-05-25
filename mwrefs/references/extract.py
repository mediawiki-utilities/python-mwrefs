import re

import mwparserfromhell

# Compile regex to parse fields
LEXEME = [
    ('ref', re.compile(r'<ref(\s[^/>]*)?/>|<ref[^/>]*>[\s\S]*?</ref>', re.M | re.I)),
    ('level_2', re.compile(r'(==[^=]+==)', re.M | re.I)),
    ('level_3', re.compile(r'(===[^=]+===)', re.M | re.I))]

GROUP_RE = re.compile(
    '|'.join('(?P<{0}>{1})'.format(name, regex.pattern)
             for name, regex in LEXEME),
    re.M | re.I)


def extract(content):
    dic = {}
    level_2, level_3 = False, False
    section = 0

    for match in GROUP_RE.finditer(content):
        if match.lastgroup == 'ref':
            dic['content'] = {}
            dic['content']['raw_content'] = match.group(0)
            dic['content']['urls'] = []
            dic['content']['identifiers'] = []

            '''
            wikicode = mwparserfromhell.parse(match[0])
            template = wikicode.filter_templates()

            if template:
                dic['content']['templated'] = True
                dic['content']['cite_template'] = template[0].name.split()[1]
                dic['content']['urls'] += template[0].get('url').value()

            else:
                dic['content']['templated'] = False
            '''

            occurrences = {}
            occurrences['section'] = section

            if not level_2 and not level_3:
                occurrences['header_level'] = 0
                occurrences['header_text'] = ''
                occurrences['header_offset'] = 0
                occurrences['level_2_text'] = ''
                occurrences['level_2_offset'] = 0

            elif level_2 and not level_3:
                occurrences['header_level'] = 2
                occurrences['header_text'] = level_2.group(0)
                occurrences['header_offset'] = level_2.span()[0]
                occurrences['level_2_text'] = level_2.group(0)
                occurrences['level_2_offset'] = level_2.span()[0]

            else:
                occurrences['header_level'] = 3
                occurrences['header_text'] = level_3.group(0)
                occurrences['header_offset'] = level_3.span()[0]
                occurrences['level_2_text'] = level_2.group(0)
                occurrences['level_2_offset'] = level_2.span()[0]

            dic['content']['occurrences'] = \
                dic['content'].get('occurrences', []) + [occurrences]

            yield dic

        else:
            if match.lastgroup == 'level_2':
                level_2 = match
                section += 1

            else:
                level_3 = match
