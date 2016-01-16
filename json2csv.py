# for ujson (to work on Windows) you need Microsoft Visual C++ Compiler for Python 2.7 to be installed:
# http://www.microsoft.com/en-us/download/details.aspx?id=44266

# more about ujson: https://pypi.python.org/pypi/ujson

import sys
import ujson as json
import csv


def flatten(structure, key="", path="", flattened=None):
    if flattened is None:
        flattened = {}
    if type(structure) not in (dict, list):
        flattened[((path + "_") if path else "") + key] = structure
        # " ".join(str(structure).strip().split())
    elif isinstance(structure, list):
        for i, item in enumerate(structure):
            flatten(item, "%d" % i, "_".join(filter(None, [path, key])), flattened)
    else:
        for new_key, value in structure.items():
            flatten(value, new_key, "_".join(filter(None, [path, key])), flattened)
    return flattened

# script works with specific JSONs.
# the goal is to transform the input JSON file in a way, where it won't start with a '{', '}' or other specific
# character not recognized with json.loads

# def joinfile(filename):
#     sarray = []
#     with open(filename) as fd:
#         for line in fd:
#             if line.startswith('{'):
#                 continue
#             sarray.append(line.rstrip('\n'))
#     return ''.join(sarray)
#
#
# aa = joinfile('test2.json')
# print(aa)

ifilename = sys.argv[1]
try:
    ofilename = sys.argv[2]
except:
    ofilename = ifilename + ".csv"

# LOAD DATA
json_lines = [json.loads(l.strip()) for l in file(ifilename).readlines()]

csv_lines = []
for l in json_lines:
    try:
        flattened = flatten(l)
        # if "business" in ifilename and len(flattened) < 10: continue
    except:
        pass
    csv_lines.append(flattened)

fieldnames = csv_lines[0].keys()
writer = csv.DictWriter(file(ofilename, "w"), fieldnames=fieldnames, delimiter="|")
writer.writerow(dict(zip(fieldnames, fieldnames)))

for entry in csv_lines:
    try:
        writer.writerow(entry)
    except Exception, e:
        print e.message
