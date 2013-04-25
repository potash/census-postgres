#!/bin/python

import os
from os.path import join


def run(data_root, working_dir):
    geo_file = open(join(working_dir, 'import_geoheader.sql'), 'w')

    for root, dirs, files in os.walk(data_root):
        for fname in files:
            if fname.startswith('g') and fname.endswith('.csv'):
                fpath = join(root, fname)
                geo_file.write("COPY tmp_geoheader FROM '%s';\n" % (fpath,))

    geo_file.close()
