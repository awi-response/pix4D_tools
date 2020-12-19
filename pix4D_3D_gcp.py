import argparse
import ee
import eeconvert
import geopandas as gpd

# Parse Arguments
parser = argparse.ArgumentParser(description='Argument parser')
parser.add_argument('-i', dest='input_file',
                    help='input file')
parser.add_argument('-o', dest='output_file',
                    help='output file')
parser.add_argument('-t_srs', dest='t_srs',
                    help='target SRS e.g. "EPSG:4326" or projected "EPSG:32605"')

args = parser.parse_args()


def main():

    ee.Initialize()

    df = gpd.read_file(args.input_file).to_crs(crs='EPSG:4326')

    fc = eeconvert.gdfToFc(df)
    arctic_dem = ee.Image("UMN/PGC/ArcticDEM/V3/2m_mosaic")
    output = arctic_dem.select("elevation").sampleRegions(collection=fc)

    agg = output.aggregate_array("elevation")

    elevation = agg.getInfo()

    df['X'] = df.to_crs(crs=args.t_srs).geometry.x
    df['Y'] = df.to_crs(crs=args.t_srs).geometry.y
    df['Z'] = elevation

    df = df.drop(columns=['geometry']).rename(columns={'id': 'LABEL'})

    df.set_index('LABEL')

    df.to_csv(args.output_file, index=False)


if __name__ == '__main__':
    main()