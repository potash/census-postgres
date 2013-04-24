#!/bin/python

import os
from os.path import join

acs_root = '/mnt/tmp/acs2010_1yr'
geoheader_sql_root = '.'

geo_file = open(join(geoheader_sql_root, 'import_geoheader.sql'), 'w')

for root, dirs, files in os.walk(acs_root):
    for fname in files:
        if fname.startswith('g') and fname.endswith('.csv'):
            fpath = join(root, fname)
            geo_file.write("COPY geoheader FROM '%s';\n" % (fpath,))

geo_file.close()
