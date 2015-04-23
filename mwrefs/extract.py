import re

REF_RE = re.compile(r'<ref(\s[^/>]*)?/>|<ref[^/>]*>[\s\S]*?</ref>', re.M|re.I)

def extract(text):
    return (m.group(0) for m in REF_RE.finditer(text))


text = """<ref>{{cite web|title=biology</ref>"""
list(extract(text))
