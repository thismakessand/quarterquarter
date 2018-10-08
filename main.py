import argparse
import logging
import sys

import fiona
from shapely.geometry import shape, mapping
from shapely.geometry.polygon import orient


from quarterquarter import quarter, quarter_quarter, quarter_quarter_quarter

operations = {
    'q': quarter,
    'qq': quarter_quarter,
    'qqq': quarter_quarter_quarter
}


def main(in_shapefile, out_shapefile, operation):
    logging.debug(in_shapefile)
    logging.debug(out_shapefile)

    with fiona.open(path=in_shapefile, driver='ESRI Shapefile') as source:
        schema = source.schema.copy()
        schema["properties"]["label"] = 'str'
        with fiona.open(out_shapefile, 'w',
            crs=source.crs['init'],
            driver="ESRI Shapefile",
            schema=schema
        ) as output:
            for row in source:
                properties = row["properties"]
                polygon = shape(row["geometry"])
                quarters = operations[operation](polygon)
                if not quarters:
                    continue
                for quarter in quarters:
                    properties["label"] = quarter.label
                    output.write({"properties": properties, "geometry": mapping(orient(quarter.polygon, sign=1.0))})
    return


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    parser = argparse.ArgumentParser(prog='quarterquarter',
                                     description='Divide polygon into quarters',
                                     usage='%(prog)s [options]')
    parser.add_argument('--operation', help='Operation (q, qq, or qqq)')
    parser.add_argument('--input_shp', help='input shapefile')
    parser.add_argument('--output_shp', help='output shapefile to be created')

    args = parser.parse_args()

    main(args.input_shp, args.output_shp, args.operation)
