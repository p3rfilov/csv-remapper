
import sys
import argparse
import textwrap


def parse_args(raw_args):
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
         Usage Examples:
            Run In Gui Mode: csv_remapper
            Run in CLI Mode: csv_remapper -t "Out-Template" -o "//output/dir" -f "file1.csv" "file2.csv" "file3.csv" ...
                  Show Help: csv_remapper -h
         '''))
    parser.add_argument('-t', '--template', type=str, help='Output Template Name')
    parser.add_argument('-d', '--out_dir', type=str, help='Output Directory')
    parser.add_argument('-f', '--files', type=str, nargs='*', help='List of CSV files to process')
    return parser.parse_args(raw_args)


def main(raw_args):
    if len(raw_args) > 1:
        from csv_remapper.components import cli
        args = parse_args(raw_args)
        cli.run_command(args)
    else:
        from csv_remapper.widgets import main_window
        main_window.main()


if __name__ == '__main__':
    main(sys.argv[1:])
