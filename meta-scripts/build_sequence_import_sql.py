#!/bin/python

import csv

acs_root = '/mnt/tmp/acs2010_1yr'
sequence_tables_sql_root = '.'


def write_one_seq_table(sql_file, cell_columns):
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

sql_file = open("%s/insert_into_tables.sql" % (sequence_tables_sql_root,), 'w')

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

    cell_names.append("NULLIF(NULLIF(%s%04d, ''), '.')::double precision" % (table_id, int(line_number)))

    if sqn is not None and prev_sqn != sqn:
        write_one_seq_table(sql_file, cell_names)
        cell_names = []
        prev_sqn = sqn

write_one_seq_table(sql_file, cell_names)
