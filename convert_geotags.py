#!/usr/bin/python3.8

# Class to convert Wingtra .json geotags to more usable formats:
#   * KML for Google Earth
#   * CSV for Excel, QGIS
#
# Usage: python convert_geotags.py path/to/geotags.json
#
# Author: Matthew Cole, 18 March 2020

import sys
import json
import os
import csv
from fastkml import kml
from shapely.geometry import Point

class ConvertGeotags:
    def check_input(self, input = None):
        if input != None:
            self.input_path = input
            self.flight_name = os.path.splitext(self.input_path)[0]
        else:
            raise Exception("Error: A path needs to be passed in")
        
        if not os.path.exists(self.input_path):
            raise Exception("Error: Not a valid path")
    
    def convert_to_list(self):
        with open(self.input_path) as json_file:
            data = json.load(json_file)

        data_out_string = []
        data_out_float = []

        for flight in data['flights']:
            for geotag in flight['geotag']:
                data_out_string.append(geotag['coordinate'])

        self.geotags_list_string = data_out_string

        for row in data_out_string:
            row_num = [float(x) for x in row]
            row_num[0], row_num[1] = row_num[1], row_num[0]
            data_out_float.append(row_num)
        
        self.geotags_list = data_out_float

    def convert_to_kml(self):  
        output_filename = self.flight_name + ".kml"

        k = kml.KML()
        ns = '{http://www.opengis.net/kml/2.2}'

        d = kml.Document(ns)
        k.append(d)
        f = kml.Folder(ns)
        d.append(f)

        i = 0
        for row in self.geotags_list:
            p = kml.Placemark(ns,str(i))
            p.geometry = Point(row)
            f.append(p)
            i += 1

        kml_file = open(output_filename, "w")
        kml_file.write(k.to_string(prettyprint=True))
        kml_file.close()

    def convert_to_csv(self):
        output_filename = self.flight_name + ".csv"

        with open(output_filename, 'w', newline="") as outfile:
            wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            wr.writerows(self.geotags_list)

    def run(self, input_path=None, kml=True, csv=True):
        self.check_input(input_path)
        self.convert_to_list()
        if kml == True: 
            self.convert_to_kml()
        if csv == True: 
            self.convert_to_csv()

if __name__ == "__main__":
    cg = ConvertGeotags()
    cg.run(sys.argv[1], kml=True, csv=True)