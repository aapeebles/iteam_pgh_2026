"""
Reads in filtering and rename variables from config and metadata
sets relevant information as environmental variables to be read in later
"""

import os
import json


with open('config.json', "r", encoding="utf-8") as f:
    data = json.load(f)

WEBURL = data.get('DATA_SOURCE')
COUNTY = data.get('COUNTY')
STATE = data.get('STATE')
# data[0]['DATA_SOURCE']

with open('metadata/columns.txt', "r",encoding="utf-8") as col_names:
    col_data = col_names.readlines()

rename_dict = {line.split(":")[0]:line.split(":")[1].rstrip("\n") for line in col_data}


os.environ['RENAME_DICT'] = json.dumps(rename_dict)
os.environ['WEBURL'] = WEBURL
os.environ['COUNTY'] = COUNTY
os.environ['STATE'] = STATE

