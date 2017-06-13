import json

from nose.tools import eq_

from ..extract import extract


def test_extract():
    content = 'These words.<ref name="foobar">{{cite web|hats}}</ref>\n' + \
              '\n' + \
              '== History ==\n' + \
              '<ref name="doesntexist"/>\n' + \
              'Here are some words too.<ref name="foobar"/>\n' + \
              '<ref name="foobar">{{cite web|hats|duplicate!}}</ref>\n' + \
              '\n' + \
              '=== Early ===\n' + \
              'He has pants.<ref name="foobar"/> ' + \
              'She runs around.<ref>Bare reference 10.1000/whatever</ref>' + \
              'They don\'t.<ref>I have a http://urlomg.com</ref>'

    reference_docs = list(extract(content))

    print(json.dumps(reference_docs, indent=2))
    eq_([rd['raw_content'] for rd in reference_docs],
        ['<ref name="foobar">{{cite web|hats}}</ref>',
         '<ref name="doesntexist"/>',
         '<ref>Bare reference 10.1000/whatever</ref>',
         '<ref>I have a http://urlomg.com</ref>'])
    eq_(reference_docs[0]['name'], "foobar")
    eq_(len(reference_docs[0]['occurrences']), 4)
    eq_(reference_docs[0]['occurrences'][0]['text_offset'], 12)
    eq_(reference_docs[2]['identifiers'], [('doi', '10.1000/whatever')])
    eq_(reference_docs[3]['urls'], ["http://urlomg.com"])
