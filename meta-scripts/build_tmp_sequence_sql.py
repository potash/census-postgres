#!/bin/python

import csv

acs_root = '/mnt/tmp/acs2010_1yr'
tmp_sequence_tables_sql_root = '.'


def write_one_seq_table(sql_file, cell_columns):
    sql_file.write("""CREATE TABLE tmp_seq%04d (
fileid varchar(6),
filetype varchar(6),
stusab varchar(2),
chariter varchar(3),
seq varchar(4),
logrecno int,
""" % (sqn,))
    sql_file.write(',\n'.join(cell_columns))
    sql_file.write("""
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);\n\n""")

sql_file = open("%s/create_import_tables.sql" % (tmp_sequence_tables_sql_root,), 'w')

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

    cell_names.append("%s%04d varchar" % (table_id, int(line_number)))

    if sqn is not None and prev_sqn != sqn:
        write_one_seq_table(sql_file, cell_names)
        cell_names = []
        prev_sqn = sqn

write_one_seq_table(sql_file, cell_names)
