# CSV 2 flare.json
# convert a csv file to flare.json for use with many D3.js viz's
# This script creates outputs a flare.json file with 2 levels of nesting.
# For additional nested layers, add them in lines 32 - 47
# sample: http://bl.ocks.org/mbostock/1283663
# csv2shapes script largely developed by andrew heekin, additions and corrections by eric d

import pandas as pd
import json


df = pd.read_csv('shapes.csv')


# choose columns to keep, in the desired nested json hierarchical order
df = df[["parent", "child", "value"]]


# order in the groupby here matters, it determines the json nesting
# the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
df1 = df.groupby(['parent', 'child'])['value'].sum()
df1 = df1.reset_index()


# start a new flare.json document
flare = dict()
d = {"name":"shape", "children": []}


for line in df1.values:
    parent = line[0]
    child = line[1]
    value = line[2]

    # make a list of keys
    keys_list = []
    for item in d['children']:
        keys_list.append(item['name'])

    # if 'the_parent' is NOT a key in the flare.json yet, append it
    if not parent in keys_list:
        d['children'].append({"name":parent, "children":[{"name":child, "size":value}]})

    # if 'the_parent' IS a key in the flare.json, add a new child to it
    else:
        d['children'][keys_list.index(parent)]['children'].append({"name":child, "size":value})

flare = d


# export the final result to a json file
with open('shapes.json', 'w') as outfile:
    json.dump(flare, outfile)