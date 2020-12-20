# point_to_3Dpix4D_GCP

This repository contains scripts to create 3D GCPs for Pix4D from Point Shapefiles.

Elevation Data (Z-values) are extracted from ArcticDEM.

The input shapefile needs to have an "id" field

Usage:
`pix4D_3D_gcp.py -i <input.shp> -o <output.csv> -t_srs EPSG:<epsg-code>` 
