#!/usr/bin/python3

# Script to convert Wingtra .json geotags to a simple .csv file
# This enables in-field plotting of geotags to ensure correct coverage
#
# Usage: python -m json_to_csv.py path/to/geotags.json
#        .csv file is output to same location as original .json
#
# Author: Matthew Cole, 03 Feb 2020

import sys
import json
import os
import csv


def check_input():
    if len(sys.argv) != 2:
        raise Exception("Error: Only one path should be input")

    if not os.path.exists(sys.argv[1]):
        raise Exception("Error: Not a valid path")


def convert():
    with open(str(sys.argv[1])) as json_file:
        data = json.load(json_file)

    data_out = []

    for flight in data['flights']:
        for geotag in flight['geotag']:
            data_out.append(geotag['coordinate'])

    output_filename = os.path.splitext(sys.argv[1])[0] + ".csv"
    with open(output_filename, 'w', newline="") as outfile:
        wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        wr.writerows(data_out)


if __name__ == "__main__":
    check_input()
    convert()
