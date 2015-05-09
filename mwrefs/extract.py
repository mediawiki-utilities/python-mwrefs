import re

REF_RE = re.compile(r'<ref(\s[^/>]*)?/>|<ref[^/>]*>[\s\S]*?</ref>', re.M|re.I)
COMMENT_RE = re.compile(r'<!--(.*?)-->')

def extract(text):
    return (m.group(0) for m in REF_RE.finditer(COMMENT_RE.sub("", text)))
