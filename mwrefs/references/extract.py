import re
import mwapi
import mwparserfromhell
from mwcites.utilities import extract as mwcites


LEXEME = [
	('ref', re.compile(r'<ref(\s[^/>]*)?/>|<ref(\s[^/>]*)?>[\s\S]*?</ref>', 
	                   re.M | re.I)), 
	('header', re.compile(r'(==[^=]+==)|(===[^=]+===)|(====[^=]+====)', 
	                      re.M | re.I))]

GROUP_RE = re.compile('|'.join('(?P<{0}>{1})'.format(name, regex.pattern) 
                               for name, regex in LEXEME), re.M | re.I)


def extract(content):
	section = 0
	header, level_2 = None, None

	for match in GROUP_RE.finditer(content):
		# Parse reference
		if match.lastgroup == 'ref':
			d = {}

			# Extract reference content
			raw_content = match.group(0)
			d['raw_content'] = raw_content 

			# Extract cite template
			wikicode = mwparserfromhell.parse(raw_content)
			templates = wikicode.filter_templates()

			# Extract template information
			if len(templates):
				d['templated'] = True
				d['cite_template'] = templates[0].name
			else:
				d['templated'] = False
				d['cite_template'] = None

			# Extract urls
			d['urls'] = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
			                       r'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
			                       raw_content, re.I)

			# Extract PubMed, DOI, ISBN, or arXiv
			_all = mwcites.ALL_EXTRACTORS
			d['identifiers'] = list(mwcites.extract_ids(raw_content, _all))

			# Extract 'name' attribute
			name = match.group(2) or match.group(3)
			if name:
				name = name.split('=')[1].strip()
			d['name'] = name
				
			# Extract occurrence information
			d['occurrences'] = []
			occurrence = {}

			# Extract section
			occurrence['section'] = section

			# Extract preceeding and succeeding texts
			s, e = match.span()
			occurrence['text_offset'] = s
			occurrence['preceding_text'] = content[max(0, s - 250):s]
			occurrence['succeeding_text'] = content[e:min(len(content), e + 250)]

			# Extract immediate and level 2 headers
			if not header and not level_2:		
				occurrence['header_level'] = 0
				occurrence['header_text'] = ''
				occurrence['header_offset'] = 0
				occurrence['level_2_text'] = ''
				occurrence['level_2_offset'] = 0
			else:
				if header == level_2:
					occurrence['header_level'] = 2
				else: 
					occurrence['header_level'] = 3
				occurrence['header_text'] = header.group(0)
				occurrence['header_offset'] = header.start()
				occurrence['level_2_text'] = level_2.group(0)
				occurrence['level_2_offset'] = level_2.start()

			# Append occurrence information
			d['occurrences'].append(occurrence)

			yield d

		# Parse header
		else:
			if match.group(5):
				header = level_2 = match
				section += 1
			elif match.group(6):
				header = match