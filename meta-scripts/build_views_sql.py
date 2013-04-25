#!/bin/python

import csv

acs_root = '/mnt/tmp/acs2010_1yr'
views_sql_root = '.'


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

sql_file = open("%s/view_stored_by_tables.sql" % (views_sql_root,), 'w')

prev_table_id = None
prev_sqn = None
cell_names = []
for row in csv.DictReader(open("%s/Sequence_Number_and_Table_Number_Lookup.txt" % acs_root, 'rU')):
    table_id = row['Table ID']
    sqn = int(row['Sequence Number'])
    line_number = row['Line Number']

    if not line_number or line_number.endswith('.5'):
        # Skip over entries that don't have line numbers because they won't have data in the sequences
        # Also skip over lines ending in .5 because they're labels
        continue

    cell_names.append("%s%04d" % (table_id, int(line_number)))

    if prev_table_id is not None and prev_table_id != table_id:
        write_one_seq_view(sql_file, prev_table_id, prev_sqn, cell_names)
        cell_names = []
        prev_table_id = table_id
        prev_sqn = sqn

write_one_seq_view(sql_file, table_id, sqn, cell_names)
