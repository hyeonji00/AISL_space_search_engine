import math
import pandas as pd
import json
from collections import OrderedDict

def conv_coor(file_data, lat, lon): 
    R = 6371
    x = R * math.cos(lat) * math.cos(lon)
    y = R * math.cos(lat) * math.sin(lon)
    z = R * math.sin(lat)

    file_data["node_locations"].append([x, y, z])

file_path = './SEJONG_NODE.csv'
data = pd.read_csv(file_path)

file_data = OrderedDict()
file_data["node_locations"] = []

for i in range(len(data)):

    longitude = data.iloc[i]['경도']
    latitude = data.iloc[i]['위도']

    conv_coor(file_data, latitude, longitude)

with open('sejong_node.json', 'w', encoding='utf-8') as make_file:
    json.dump(file_data, make_file, ensure_ascii=False, indent='\t')

