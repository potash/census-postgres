#!/bin/python

import csv
from itertools import groupby

acs_root = '/mnt/tmp/acs2010_1yr'
sequence_tables_sql_root = '.'


def write_one_seq_table(sql_file, sqn, cell_columns):
    sql_file.write("""INSERT INTO seq%04d
SELECT fileid, filetype, upper(stusab), chariter, seq, logrecno::int,
""" % (sqn,))
    sql_file.write(',\n'.join(cell_columns))
    sql_file.write("""
FROM tmp_seq%04d;\n\n""" % (sqn,))

    # A tiny hack to append "_moe" to the name of the column
    cell_moe_columns = [t.replace(", ''", "_moe, ''") for t in cell_columns]

    sql_file.write("""INSERT INTO seq%04d_moe
SELECT fileid, filetype, upper(stusab), chariter, seq, logrecno::int,
""" % (sqn,))
    sql_file.write(',\n'.join(cell_moe_columns))
    sql_file.write("""
FROM tmp_seq%04d_moe;\n\n""" % (sqn,))


def run(data_root, working_dir, config):
    sqn_col_name = config['sequence_number_column_name']
    line_no_col_name = config['line_number_column_name']

    sql_file = open("%s/insert_into_tables.sql" % (working_dir,), 'w')

    sqn_lookup_file = csv.DictReader(open("%s/Sequence_Number_and_Table_Number_Lookup.txt" % data_root, 'rU'))
    cell_names = []
    prev_line_number = 0
    for sqn, rows in groupby(sqn_lookup_file, key=lambda row: int(row[sqn_col_name])):
        for row in rows:
            table_id = row['Table ID']
            line_number = row[line_no_col_name]

            if not line_number or line_number.endswith('.5') or line_number == '.':
                # Skip over entries that don't have line numbers because they won't have data in the sequences
                # Also skip over lines ending in .5 because they're labels
                continue

            line_number = int(line_number)

            if (line_number - prev_line_number) != 1 and (line_number != 1):
                # In 2009 it looks like they screwed up the .5 label thing
                #   and the only way to detect a label is to ensure the line
                #   number increments by one
                # We also want to let the line number reset back to 1 mid-sequence
                continue

            cell_names.append("NULLIF(NULLIF(%s%04d, ''), '.')::double precision" % (table_id, line_number))
            prev_line_number = line_number

        write_one_seq_table(sql_file, sqn, cell_names)
        cell_names = []
        prev_line_number = 0
