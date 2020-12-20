import argparse
import ee
import eeconvert
import geopandas as gpd

# Parse Arguments
parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument('-i', dest='input_file', required=True,
                    help='input file')
parser.add_argument('-o', dest='output_file', required=True,
                    help='output file')
parser.add_argument('-t_srs', dest='t_srs', default='EPSG:4326',
                    help='target SRS e.g. "EPSG:4326" or projected "EPSG:32605"')

args = parser.parse_args()


def main():
    df = gpd.read_file(args.input_file).to_crs(crs='EPSG:4326')

    # Read elevation from Arctic DEM in Google Earthengine
    ee.Initialize()
    fc = eeconvert.gdfToFc(df)
    arctic_dem = ee.Image("UMN/PGC/ArcticDEM/V3/2m_mosaic")
    output = arctic_dem.select("elevation").sampleRegions(collection=fc)
    agg = output.aggregate_array("elevation")
    elevation = agg.getInfo()

    # write coordinates and elevation
    df['X'] = df.to_crs(crs=args.t_srs).geometry.x
    df['Y'] = df.to_crs(crs=args.t_srs).geometry.y
    df['Z'] = elevation

    # columns settings
    df = df.drop(columns=['geometry']).rename(columns={'id': 'LABEL'})
    df.set_index('LABEL')
    # output to csv file
    df.to_csv(args.output_file, index=False)


if __name__ == '__main__':
    main()
