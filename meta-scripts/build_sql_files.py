#!/bin/python

# This script builds the plsql files required to generate a `census-postgres`-style
# database for any arbitrary ACS dataset.
#
# This assumes that you've downloaded the "All in 1 Giant File" zip files, unpacked
# them somewhere, and placed the "Sequence_Number_and_Table_Number_Lookup.txt" file
# in the same directory as the unpacked files. The directory with those files is
# referred to as the `acs_root` variable in this program.
#
# The comments below that begin with ... represent the various SQL files that need
# to be generated to complete the import and how they're built in this script.

acs_root = '/mnt/tmp/acs2011_1yr'
working_dir = '.'

##
## The generated SQL in this section creates the schema for the data to be copied
## in to. It should run fairly quick and generate a few thousand tables in your DB.
##

# ... create_geoheader.sql: doesn't change and should be copied

# ... geoheader_comments.sql: doesn't change and should be copied

# ... create_tmp_geoheader.sql: doesn't change and should be copied

# ... drop_import_tables.sql: drops any existing tmp_* or tmp_*_moe tables
#                             in preparation for importing new ones
import build_drop_import_tables_sql
build_drop_import_tables_sql.run(acs_root, working_dir)

# ... create_import_tables.sql: builds the tmp_* and tmp_*_moe tables
#                               that will be imported into with COPY commands
import build_tmp_sequence_sql
build_tmp_sequence_sql.run(acs_root, working_dir)

##
## The generated SQL in this section actually performs the loading into the tables
## that were created above using a bunch of COPY statements.
##

# ... import_geoheader.sql: COPYs the geometry files to the tmp_geoheader table
import build_geoheader_import_sql
build_geoheader_import_sql.run(acs_root, working_dir)

# ... import_sequences.sql: COPYs the estimate and moe data into the tmp_* and tmp_*_moe tables
import build_tmp_sequence_import_sql
build_tmp_sequence_import_sql.run(acs_root, working_dir)

# ... parse_tmp_geoheader.sql: parses the tmp_geoheader table into the geoheader table
# (Should be copied from another year)

# ... store_by_tables.sql: builds the sequence-based (not tmp_*) tables
#                          you might wonder why we're building tmp* then dumping
#                          straight into real tables. I did this because the original
#                          author did it so he could experiment with other storage
#                          idioms and I wanted to be flexible like that too.
import build_sequence_sql
build_sequence_sql.run(acs_root, working_dir)

# ... insert_into_tables.sql: inserts the data from the tmp_* tables into the
#                             appropriate seq_* tables.
import build_sequence_import_sql
build_sequence_import_sql.run(acs_root, working_dir)

# ... view_stored_by_tables.sql: creates views for each ACS table based on the sequences
import build_views_sql
build_views_sql.run(acs_root, working_dir)
