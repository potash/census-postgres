"""
The 2007 releases seem to have trailing empty columns truncated from some of the
sequences, breaking the import into PostgreSQL. This is designed to "even out"
the CSV files so that they have a consistent number of columns.
"""

from optparse import OptionParser
from csv import reader, writer

parser = OptionParser()
parser.set_defaults(nullchar='')

parser.add_option('-c', '--columns', dest='columns', help='Target column count', type='int')
parser.add_option('-n', '--nullchar', dest='nullchar', help='Null characters, default empty string')

if __name__ == '__main__':

    opts, (infile, outfile) = parser.parse_args()

    if opts.columns is None:
        columns = max([len(row) for row in reader(open(infile))])
    else:
        columns = opts.columns

    output = writer(open(outfile, 'w'))

    for row in reader(open(infile)):
        if len(row) < columns:
            row += [opts.nullchar] * (columns - len(row))

        output.writerow(row[:columns])