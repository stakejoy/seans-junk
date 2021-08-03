import requests
import json
import time
import pandas as pd
import numpy as np
import plotly.express as px

v_data = []
final_data = []
addr_list = []

with open("shit.list", "r") as fd:
    for line in fd:
        line = line.replace("\r", "").replace("\n", "").replace(" ","")
        addr_list.append(line)

def get_data(cursor):
    if (cursor != "none"): 
        uri =  "https://api.helium.io/v1/validators?cursor="+cursor
    else: 
        uri =  "https://api.helium.io/v1/validators"
    
    r = requests.get(uri)
    data = json.loads(r.text)
    for d in data['data']:
        v_data.append(d)
    if ("cursor" in data):
        get_data(data['cursor'])

get_data("none")
for v in v_data: 
    if (v['status']['online'] == "online"):
        for p in v['penalties']:
            if p['type'] == 'dkg':
                print(v['address'])
            if v['address'] in addr_list:
                if p['type'] == 'dkg':
                    p['type'] = 'shitlist_dkg'
                if p['type'] != 'tenure' and p['type'] != 'shitlist_dkg':
                    p['type'] = "shitlist"
            rec = [v['address'],v['version_heartbeat'],p['height'], p['type'],p['amount']]
            final_data.append(rec)

df = pd.DataFrame(final_data, columns = ['address','version_heartbeat','height', 'type', 'amount'])

fig = px.scatter(df, x="height", y="amount", color="type",
                 size='amount', hover_data=['address','version_heartbeat'], template='ggplot2')
fig.show()
