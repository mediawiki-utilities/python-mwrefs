"""
Extracts reference tags from Wikipedia XML database dumps.

Generates a TSV dataset with one row per revision with the following fields.

* page_id
* page_title
* rev_id
* rev_timestamp
* ref_tag

Usage:
    extract -h | --help
    extract <dump-file>...

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

            for revision in page:
                for reference in set(extract(revision.text or "")):

                    yield (page.id, page.title, revision.id, revision.timestamp,
                           reference)


    print("\t".join(["page_id", "page_title", "rev_id", "rev_timestamp",
                     "reference"]))

    for vals in xml_dump.map(dump_files, process_dump):
        print("\t".join(tsv_encode(val) for val in vals))
