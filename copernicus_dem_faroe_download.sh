# !/bin/bash

#-----------------------------------------------------------------------------#
# Copernicus DEM tiles for Faroe Islands
#-----------------------------------------------------------------------------#
#
# Area          : Faroe Islands
# Resolution    : 30m
# Tiles needed  : N61 W007, N61 W008, N62 W007, N62 W008
# Source        : s3://eodata/auxdata/CopDEM_COG/copernicus-dem-30m/
# Reference     : https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM
# Date          : 2024-06-10
# Author        : Ole Lindberg, oli@dmi.dk, Danish Meteorological Institute
# Prerequisites : s3cmd installed and configured (see below)
# Usage         : ./copernicus_dem_faroe_download.sh
#
#-----------------------------------------------------------------------------#
#
# The available DEM tiles can be found here:
#
# https://s3.waw3-1.cloudferro.com/swift/v1/portal_uploads_prod/GEO1988-CopernicusDEM-RP-002_GridFile_I6.0.shp_08.2024.zip
#
#-----------------------------------------------------------------------------#
#
# s3 Configuration:
#
# s3 key and secret must be obtained from Copernicus Data Space:
# https://eodata-s3keysmanager.dataspace.copernicus.eu/panel/s3-credentials
#
# s3cmd configuration file (~/.s3cfg) should look like this:
#
# [default]
# access_key = <ACCESS_KEY>
# host_base = eodata.dataspace.copernicus.eu
# host_bucket = eodata.dataspace.copernicus.eu
# human_readable_sizes = False
# secret_key = <SECRET_KEY>
# use_https = true
# check_ssl_certificate = true
#
#-----------------------------------------------------------------------------#

mkdir -p data/copernicus_dem_faroe
cd data/copernicus_dem_faroe

s3cmd -c ~/.s3cfg get s3://eodata/auxdata/CopDEM_COG/copernicus-dem-30m/Copernicus_DSM_COG_10_N61_00_W007_00_DEM/Copernicus_DSM_COG_10_N61_00_W007_00_DEM.tif
s3cmd -c ~/.s3cfg get s3://eodata/auxdata/CopDEM_COG/copernicus-dem-30m/Copernicus_DSM_COG_10_N61_00_W008_00_DEM/Copernicus_DSM_COG_10_N61_00_W008_00_DEM.tif
s3cmd -c ~/.s3cfg get s3://eodata/auxdata/CopDEM_COG/copernicus-dem-30m/Copernicus_DSM_COG_10_N62_00_W008_00_DEM/Copernicus_DSM_COG_10_N62_00_W008_00_DEM.tif
s3cmd -c ~/.s3cfg get s3://eodata/auxdata/CopDEM_COG/copernicus-dem-30m/Copernicus_DSM_COG_10_N62_00_W007_00_DEM/Copernicus_DSM_COG_10_N62_00_W007_00_DEM.tif
 
cd ../../