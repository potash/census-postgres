#!/bin/python

import csv
from itertools import groupby


def write_one_seq_view(sql_file, table_id, sqn, cell_columns):
    sql_file.write("""CREATE VIEW %s AS SELECT
stusab, logrecno,
""" % (table_id,))
    sql_file.write(',\n'.join(cell_columns))
    sql_file.write("\nFROM seq%04d;\n\n" % sqn)

    # A tiny hack to append "_moe" to the name of the column
    cell_moe_columns = ["%s, %s_moe" % (t, t) for t in cell_columns]

    sql_file.write("""CREATE VIEW %s_moe AS SELECT
stusab, logrecno,
""" % (table_id,))
    sql_file.write(',\n'.join(cell_moe_columns))
    sql_file.write("\nFROM seq%04d JOIN seq%04d_moe USING (stusab, logrecno);\n\n" % (sqn, sqn))


def run(data_root, working_dir, config):
    sqn_col_name = config['sequence_number_column_name']
    line_no_col_name = config['line_number_column_name']

    sql_file = open("%s/view_stored_by_tables.sql" % (working_dir,), 'w')

    sqn_lookup_file = csv.DictReader(open("%s/Sequence_Number_and_Table_Number_Lookup.txt" % data_root, 'rU'))
    cell_names = []
    for table_id, rows in groupby(sqn_lookup_file, key=lambda row: row['Table ID']):
        for row in rows:
            sqn = int(row[sqn_col_name])
            line_number = row[line_no_col_name]

            if not line_number or line_number.endswith('.5') or line_number == '.' or (row['Table Title'].endswith('--') and line_number.endswith('5')):
                # Skip over entries that don't have line numbers because they won't have data in the sequences
                # Also skip over lines ending in .5 because they're labels
                # In 2009 it looks like they screwed up the .5 label thing
                #   and the only way to detect it is with a '-- ' at the end of the title
                continue

            cell_names.append("%s%04d" % (table_id, int(line_number)))

        write_one_seq_view(sql_file, table_id, sqn, cell_names)
        cell_names = []
