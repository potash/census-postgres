#!/bin/python

import csv
from itertools import groupby


def run(data_root, working_dir, config):
    sqn_col_name = config['sequence_number_column_name']

    sql_file = open("%s/drop_import_tables.sql" % (working_dir,), 'w')

    sqn_lookup_file = csv.DictReader(open("%s/Sequence_Number_and_Table_Number_Lookup.txt" % data_root, 'rU'))
    for sqn, rows in groupby(sqn_lookup_file, key=lambda row: int(row[sqn_col_name])):
        sql_file.write("DROP TABLE IF EXISTS tmp_seq%04d;\n" % (sqn,))
        sql_file.write("DROP TABLE IF EXISTS tmp_seq%04d_moe;\n" % (sqn,))

    sql_file.close()
