#!/bin/python

import csv
from itertools import groupby


def write_one_seq_view(sql_file, table_id, sqn, cell_columns):
    sql_file.write("""CREATE VIEW %s (
stusab, logrecno,
""" % (table_id,))
    sql_file.write(',\n'.join(cell_columns))
    sql_file.write("\nFROM seq%04d;\n\n" % sqn)

    # A tiny hack to append "_moe" to the name of the column
    cell_moe_columns = ["%s_moe" % t for t in cell_columns]

    sql_file.write("""CREATE VIEW %s_moe (
stusab, logrecno,
""" % (table_id,))
    sql_file.write(',\n'.join(cell_moe_columns))
    sql_file.write("\nFROM seq%04d_moe;\n\n" % sqn)


def run(data_root, working_dir, config):
    sql_file = open("%s/view_stored_by_tables.sql" % (working_dir,), 'w')

    sqn_lookup_file = csv.DictReader(open("%s/Sequence_Number_and_Table_Number_Lookup.txt" % data_root, 'rU'))
    cell_names = []
    for table_id, rows in groupby(sqn_lookup_file, key=lambda row: row['Table ID']):
        for row in rows:
            sqn = int(row['Sequence Number'])
            line_number = row['Line Number']

            if not line_number or line_number.endswith('.5'):
                # Skip over entries that don't have line numbers because they won't have data in the sequences
                # Also skip over lines ending in .5 because they're labels
                continue

            cell_names.append("%s%04d" % (table_id, int(line_number)))

    write_one_seq_view(sql_file, table_id, sqn, cell_names)
    cell_names = []
