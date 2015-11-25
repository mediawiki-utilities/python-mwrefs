import argparse
import subprocess
import codecs
import os

import mw.xml_dump
import mwxml
import pathlib

from . import utils, processors


def open_xml_file(path):
    f = mw.xml_dump.functions.open_file(
        mw.xml_dump.functions.file(path)
    )
    return f


def compressor_7z(file_path):
    p = subprocess.Popen(
        ['7z', 'a', '-si', file_path],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
    utf8writer = codecs.getwriter('utf-8')

    return utf8writer(p.stdin)


def output_writer(path, compression):
    if compression == '7z':
        return compressor_7z(path + '.7z')
    else:
        return open(path, 'wt', encoding='utf-8')


def create_path(path):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)


def get_args():
    parser = argparse.ArgumentParser(
        prog='wikidump',
        description='Wikidump features extractor.',
    )
    parser.add_argument('files',
        metavar='FILE',
        type=pathlib.Path,
        nargs='+',
        help='XML Wikidump file to parse. It accepts only 7z.'
    )
    parser.add_argument('output_dir_path',
        metavar='OUTPUT_DIR',
        type=pathlib.Path,
        help='XML output directory.',
    )
    parser.add_argument('--output-compression',
        choices={None, '7z'},
        required=False,
        default=None,
        help='Output compression format.',
    )
    parser.add_argument('--dry-run', '-n',
        action='store_true',
        help="Don't write any file",
    )

    subparsers = parser.add_subparsers(help='sub-commands help')
    processors.bibliography_extractor.configure_subparsers(subparsers)
    processors.identifiers_extractor.configure_subparsers(subparsers)
    processors.sections_counter.configure_subparsers(subparsers)

    parsed_args = parser.parse_args()
    if 'func' not in parsed_args:
        parser.print_usage()
        parser.exit(1)

    return parsed_args


def main():
    args = get_args()

    args.output_dir_path.mkdir(parents=True, exist_ok=True)

    for input_file_path in args.files:
        utils.log("Analyzing {}...".format(input_file_path))

        dump = mwxml.Dump.from_file(open_xml_file(str(input_file_path)))

        basename = input_file_path.name

        if args.dry_run:
            pages_output = open(os.devnull, 'wt')
            stats_output = open(os.devnull, 'wt')
        else:
            pages_output = output_writer(
                path=str(args.output_dir_path/(basename + '.features.xml')),
                compression=args.output_compression,
            )
            stats_output = output_writer(
                path=str(args.output_dir_path/(basename + '.stats.xml')),
                compression=args.output_compression,
            )
        args.func(dump,
            pages_output,
            stats_output,
            args,
        )


if __name__ == '__main__':
    main()
