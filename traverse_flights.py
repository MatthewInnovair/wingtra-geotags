#!/usr/bin/python3

# Script to traverse over individual flights in a WingtraPilotProjects folder
# Calls json_to_csv.py and prints paths to geotags to console
#
# Usage: python traverse_flights.py path/to/WingtraPilotProjects
#
# Author: Matthew Cole, 17 March 2020

import sys
import os
from glob import glob


def check_input():
    if os.path.exists(os.path.join(sys.argv[1], "WingtraPilotProjects")):
        path = os.path.join(sys.argv[1], "WingtraPilotProjects")
    elif not os.path.exists(sys.argv[1]):
        raise Exception("Error: Not a valid path")
    else:
        path = sys.argv[1]
    return path

def get_path_to_geotags(path):
    # get list of containing folders
    flights = glob(os.path.join(path,"./*/"))

    for f in flights:
        # workaround for Wingtra folder structure
        data_path = os.path.join(f, "DATA")
        flight_name = os.path.basename(os.path.normpath(f))
        geotag_path = os.path.join(data_path, flight_name + ".json")

        # check guess at geotag path exists and perform actions
        if os.path.exists(geotag_path):
            print(geotag_path)
            os.system("python json_to_csv.py " + geotag_path)    

if __name__ == "__main__":
    path = check_input()
    get_path_to_geotags(path)