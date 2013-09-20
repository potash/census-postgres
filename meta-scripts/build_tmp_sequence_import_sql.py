#!/bin/python

import os
from os.path import join


def run(data_root, working_dir, release, config):
    sql_file = open("%s/import_sequences.sql" % working_dir, 'w')

    estimate_sequences = []
    moe_sequences = []

    for root, dirs, files in os.walk(data_root):
        files.sort()

        for fname in files:
            fpath = join(root, fname)

            if fname.startswith('e') and fname.endswith('.txt'):
                sqn = int(fname[8:12])
                estimate_sequences.append((sqn, fpath))
            elif fname.startswith('m') and fname.endswith('.txt'):
                sqn = int(fname[8:12])
                moe_sequences.append((sqn, fpath))

    for (sqn, fpath) in sorted(estimate_sequences):
        sql_file.write("COPY %s.tmp_seq%04d FROM '%s' WITH CSV;\n" % (release, sqn, fpath))

    for (sqn, fpath) in sorted(moe_sequences):
        sql_file.write("COPY %s.tmp_seq%04d_moe FROM '%s' WITH CSV;\n" % (release, sqn, fpath))

    sql_file.close()
