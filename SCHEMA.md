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


