'''
    This is a random take at building perf to tensure from the helium API. 
    It may or may not work for your needs. 
'''

import requests
import json

v_data = []

def get_data(cursor='none'):
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
ten = 0
pen = 0
get_data()
for v in v_data: 
    if (v['stake_status'] == "staked"):
        for p in v['penalties']:
            if p['type'] == 'dkg':
                pen = pen+1
            if p['type'] == 'performance':
                pen = pen+p['amount']
            if p['type'] == 'tenure':
                ten = ten+0.5

print(pen/ten)
