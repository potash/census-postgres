Census Postgres Schema
======================

This document describes the schema for the census-postgres project.

Contents
--------

The primary purpose for this database is to store [American Community Survey](http://www.census.gov/acs/www/)
(ACS) data in an easily queryable schema. Similar data (like the Decennial Census)
could fit in here, too.

Overview
--------

There is one PostgreSQL schema for each ACS release. The data itself is stored in
PostgreSQL tables corresponding to the ACS sequence numbers. PostgreSQL views
pointing to the correct columns in the sequence tables are then created for each
ACS table. There are also views that contain the MOE for each ACS column alongside
the actual data.

In addition to the actual data, each release schema contains two useful PostgreSQL
tables with metadata about the release. First is the `geoheader` containing
information about the GEOID name for the various geographies used in the ACS data.
Second is `census_table_metadata` describing each ACS column in every ACS table.

The Census Reporter project's EBS snapshot also contains [TIGER 2012](http://www.census.gov/geo/education/howtos.html)
data in a PostGIS database. This allows you to make maps and correlate the ACS
data with physical areas in the country.

ACS Data Tables
---------------

Data is retrieved by fetching the summary file, the table "shells" XLS, and "lookup"
XLS from the Census website (e.g. the [2011 1-year sumamry file](http://www2.census.gov/acs2011_1yr/summaryfile/)).
[Scripts](https://github.com/censusreporter/census-postgres/tree/master/meta-scripts)
are used to consume this raw data and turn it into consistent SQL statements for
import into a PostgreSQL database.

Each ACS sequence contains at least one ACS table. Each ACS table contains one or more
columns of data along with a matching "measurement of error" (MOE) column. The
scripts create PostgreSQL tables for each ACS sequence and then creates views for
each ACS table, pulling the sequences apart into the tables. Each table is keyed
with a `stusab` (state abbreviation) and `logrecno` (a record number). These two values
are found in the `geoheader` for the area you're interested in.

ACS Metadata Table
------------------

The scripts that create the data tables also store informaton about the tables and columns
themselves in the `census_table_metadata` table. You can get table and column names along
with column heirarchy information out of this table. It is keyed off of the column ID.

TIGER 2012 Tables
-----------------

The Census tabulation-related data from TIGER 2012 is loaded in the `tiger2012` schema
using PostGIS.
