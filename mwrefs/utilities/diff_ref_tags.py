"""
Extracts reference diffs from Wikipedia XML database dumps.

Generates a TSV dataset with one row per revision with the following fields.

* rev_id
* rev_timestamp
* user_id
* user_text
* page_id
* page_title
* references_added (a list of complete "<ref>...</ref>" and '<ref name="..."/>' tags)
* references_removed (a list of complete "<ref>...</ref>" and '<ref name="..."/>' tags)

Note that only revisions where a change in reference happens will be reported.
References added/removed are detected by performing a set difference on the
references that appear in two sequential revisions:

Let R be a set of reference tags and Rn be the set of reference tags in
revision n.

* references_added = Rn+1 - Rn
* references_removed = Rn - Rn+1

Usage:
    diffs -h | --help
    diffs <dump-file>...

Options:
    -h --help    Prints this documentation
    <dump-file>  Path to a set of XML dumps files (pages meta history)
"""
import json
import sys

import docopt
from mw import xml_dump

from ..extract import extract
from .util import tsv_encode


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)

    dump_files = args['<dump-file>']

    run(dump_files)

def run(dump_files):

    def process_dump(dump, path):
        for page in dump:
            if page.namespace != 0: continue

            last_references = set()
            for revision in page:

                references = set(extract(revision.text or ""))

                references_added = references - last_references
                references_removed = last_references - references

                if len(references_added) > 0 or len(references_removed) > 0:
                    if revision.contributor:
                        user_id = revision.contributor.id
                        user_text = revision.contributor.user_text
                    else:
                        user_id = 0
                        user_text = None

                    yield (revision.id, revision.timestamp, user_id, user_text,
                           page.id, page.title, list(references_added),
                           list(references_removed))

                last_references = references

    print("\t".join(["rev_id", "rev_timestamp", "user_id", "user_text",
                     "page_id", "page_title", "references_added",
                     "references_removed"]))

    for vals in xml_dump.map(dump_files, process_dump):
        print("\t".join(tsv_encode(val) for val in vals))
