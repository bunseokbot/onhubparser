from argparse import ArgumentParser

import diagnosticreport_pb2 as diagnostic


def main(args, parser):
    if args.report_file is None:
        print('[ERROR] Google OnHub diagnostic report file required')
        parser.print_usage()
        return


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-r', '--report-file', dest='report_file',
        help='Path of Google OnHub diagnostic report file')
    parser.add_argument('-o', '--output-file', dest='output_file',
        help='Path of Google OnHub diagnostic report output file')

    args = parser.parse_args()
    main(args, parser)
