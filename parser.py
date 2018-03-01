"""Google OnHub diagnositc report parser."""
from argparse import ArgumentParser
from zlib import decompress, MAX_WBITS
from base64 import b64encode

import diagnosticreport_pb2 as diagnostic
import json


class OnhubParser(dict):
    """Onhub Diagnostic Report parser."""

    def __init__(self, filepath):
        """Initializing parser."""
        dr = diagnostic.DiagnosticReport()
        dr.ParseFromString(open(filepath, 'rb').read())

        self.report = self.generate_report(dr)

    def generate_report(self, dr):
        """Generate JSON report."""
        result = {
            'version': dr.version,
            'whirlwindVersion': dr.whirlwindVersion,
            'stormVersion': dr.stormVersion,
            'unknown1': dr.unknown1,
            'unixTime': dr.unixTime,
            'infoJSON': json.loads(dr.infoJSON),
            'networkConfig': dr.networkConfig,
            'wanInfo': dr.wanInfo,
            'commandOutput': [],
            'unknownPairs': [],
            'fileLengths': [],
            'files': [],
        }

        # add command outputs
        for command in dr.commandOutputs:
            result['commandOutput'].append({
                'command': command.command,
                'output': command.output
            })

        # add unknown pairs
        for pair in dr.unknownPairs:
            result['unknownPairs'].append({
                'unknown1': pair.unknown1,
                'unknown2': pair.unknown2
            })

        # add file lengths
        for file in dr.fileLengths:
            result['fileLengths'].append({
                'path': file.path,
                'length': file.length
            })

        # add file data
        for file in dr.files:
            try:
                result['files'].append({
                    'path': file.path,
                    'content': b64encode(decompress(file.content, 16 + MAX_WBITS)).decode()
                })
            except:
                result['files'].append({
                    'path': file.path,
                    'content': b64encode(file.content).decode()
                })

        return result

    def write_file(self, output_file):
        """Write report to file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.report))

    def __del__(self):
        """Destruct parser."""
        del self


def main(args, parser):
    """Main method of onhub parser."""
    if args.report_file is None:
        print('[ERROR] Google OnHub diagnostic report file required')
        parser.print_usage()
        return

    op = OnhubParser(args.report_file)

    if args.output_file:
        op.write_file(args.output_file)

    del op


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-r', '--report-file', dest='report_file',
                        help='Path of Google OnHub diagnostic report file')
    parser.add_argument('-o', '--output-file', dest='output_file',
                        help='Path of Google OnHub diagnostic report output file')

    args = parser.parse_args()
    main(args, parser)
