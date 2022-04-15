
import os

from csv_remapper.components import io_handlers, remappers

# noinspection PyUnreachableCode
if False:
    import argparse


def run_command(args):  # type: (argparse.Namespace) -> None
    _check_args(args)
    handler = io_handlers.AppDirectoryHandler()
    if not os.path.isdir(handler.root):
        raise Exception('Template Storage location not set. Please run the tool in GUI mode and follow instructions')
    remapped_files = []
    for csv_file in args.files:
        data = remappers.remap_csv_file(csv_file, args.template, handler)
        new_file = io_handlers.write_remapped_data(csv_file, args.out_dir, data)
        remapped_files.append(f'"{new_file}"')
    print(' '.join(remapped_files))  # output results to stdout


def _check_args(args):
    if not args.out_dir:
        raise Exception('Output Directory not provided')
    if not args.template:
        raise Exception('Output Template not provided')
    if not args.files:
        raise Exception('CSV files not provided')
    if not os.path.isdir(args.out_dir):
        raise Exception(f'Directory does not exist: "{args.out_dir}"')
    for f in args.files:
        if not os.path.isfile(f):
            raise Exception(f'File not found: "{f}"')
