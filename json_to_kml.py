#!/usr/bin/python3.8

# Script to convert Wingtra .json geotags to a simple .kml file
#
# Usage: python json_to_kml.py path/to/geotags.json
#
# Author: Matthew Cole, 18 March 2020

import sys
import json
import os
from fastkml import kml
from shapely.geometry import Point

def check_input():
    if len(sys.argv) != 2:
        raise Exception("Error: Only one path should be input")

    if not os.path.exists(sys.argv[1]):
        raise Exception("Error: Not a valid path")


def convert_to_list():
    with open(str(sys.argv[1])) as json_file:
        data = json.load(json_file)

    data_out = []

    for flight in data['flights']:
        for geotag in flight['geotag']:
            data_out.append(geotag['coordinate'])
    
    return data_out

def convert_to_kml(geotags):
    flight_name = os.path.splitext(sys.argv[1])[0]
    output_filename = flight_name + ".kml"

    k = kml.KML()
    ns = '{http://www.opengis.net/kml/2.2}'

    d = kml.Document(ns)
    k.append(d)
    f = kml.Folder(ns)
    d.append(f)

    i = 0
    for row in geotags:
        row_num = [float(tag) for tag in row]
        row_num[0], row_num[1] = row_num[1], row_num[0]

        p = kml.Placemark(ns,str(i))
        p.geometry = Point(row_num)
        f.append(p)
        i += 1

    kml_file = open(output_filename, "w")
    kml_file.write(k.to_string(prettyprint=True))
    kml_file.close()


if __name__ == "__main__":
    check_input()
    geotags = convert_to_list()
    geotags_kml = convert_to_kml(geotags)
