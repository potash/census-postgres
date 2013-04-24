#!/bin/python

import os
from os.path import join

acs_root = '/mnt/tmp/acs2010_1yr'
tmp_sequence_tables_sql_root = '.'

sql_file = open("%s/import_sequences.sql" % tmp_sequence_tables_sql_root, 'w')

for root, dirs, files in os.walk(acs_root):
    files.sort()

    for fname in files:
        fpath = join(root, fname)

        if fname.startswith('e') and fname.endswith('.txt'):
            # Write out the estimate COPY lines
            sqn = int(fname[8:12])
            sql_file.write(
                "COPY tmp_seq%04d FROM '%s' WITH CSV;\n" % (sqn, fpath))
        elif fname.startswith('m') and fname.endswith('.txt'):
            # Write out the MOE COPY lines
            sqn = int(fname[8:12])
            sql_file.write(
                "COPY tmp_seq%04d_moe FROM '%s' WITH CSV;\n" % (sqn, fpath))

sql_file.close()
