#!/bin/python

import csv
from itertools import groupby


def write_one_seq_table(sql_file, sqn, cell_columns):
    sql_file.write("""CREATE TABLE seq%04d (
fileid varchar(6),
filetype varchar(6),
stusab varchar(2),
chariter varchar(3),
seq varchar(4),
logrecno int,
""" % (sqn,))
    sql_file.write(',\n'.join(cell_columns))
    sql_file.write(""",
PRIMARY KEY (stusab, logrecno)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);\n\n""")

    # A tiny hack to append "_moe" to the name of the column
    cell_moe_columns = [t.replace(' do', '_moe do') for t in cell_columns]

    sql_file.write("""CREATE TABLE seq%04d_moe (
fileid varchar(6),
filetype varchar(6),
stusab varchar(2),
chariter varchar(3),
seq varchar(4),
logrecno int,
""" % (sqn,))
    sql_file.write(',\n'.join(cell_moe_columns))
    sql_file.write(""",
PRIMARY KEY (stusab, logrecno)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);\n\n""")


def run(data_root, working_dir, config):
    sqn_col_name = config['sequence_number_column_name']
    line_no_col_name = config['line_number_column_name']

    sql_file = open("%s/store_by_tables.sql" % (working_dir,), 'w')

    sqn_lookup_file = csv.DictReader(open("%s/Sequence_Number_and_Table_Number_Lookup.txt" % data_root, 'rU'))
    cell_names = []
    for sqn, rows in groupby(sqn_lookup_file, key=lambda row: int(row[sqn_col_name])):
        for row in rows:
            table_id = row['Table ID']
            line_number = row[line_no_col_name]

            if not line_number or line_number.endswith('.5') or line_number == '.' or (row['Table Title'].endswith('--') and line_number.endswith('5')):
                # Skip over entries that don't have line numbers because they won't have data in the sequences
                # Also skip over lines ending in .5 because they're labels
                # In 2009 it looks like they screwed up the .5 label thing
                #   and the only way to detect it is with a '-- ' at the end of the title
                continue

            cell_names.append("%s%04d double precision" % (table_id, int(line_number)))

        write_one_seq_table(sql_file, sqn, cell_names)
        cell_names = []
