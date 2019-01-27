#!/user/bin/python

import argparse
from family import Family

# Set up arguments needed for running the program
parser = argparse.ArgumentParser(description="Tests the Python JCONF tool")
parser.add_argument("file", 
					help="Name of JSON file")
args = parser.parse_args()

# Actually open the file.
with open(args.file, 'r') as f:
    json_data = f.read()
    fam = Family()
    result = fam.parse_string(json_data)
    print(result)