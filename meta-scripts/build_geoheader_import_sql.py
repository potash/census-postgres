#!/bin/python

import os
from os.path import join


def run(data_root, working_dir, release, config):
    geo_file = open(join(working_dir, 'import_geoheader.sql'), 'w')

    for root, dirs, files in os.walk(data_root):
        for fname in files:
            if fname.startswith('g') and fname.endswith('.txt'):
                fpath = join(root, fname)
                geo_file.write("COPY %s.tmp_geoheader FROM '%s' WITH ENCODING 'latin1';\n" % (release, fpath,))

    geo_file.close()
