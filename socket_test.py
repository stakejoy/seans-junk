import http.client
import requests
import json
import time
import re
import socket
import time


v_data = []
ip_addresses = []


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
    if v['status']['online'] == 'online' and v['status']['height'] != None:
        if v['status']['height']  > 940000:
            ip = v['status']['listen_addrs']
            if ip != None:
                for i in ip:
                    try:
                        addr = re.search(r'ip4/(.*)/tcp', i)
                        port = re.search(r'tcp/(.*)',i)
                    except:
                        continue
                    NoneType = type(None)
                    if isinstance(addr, re.Match):
                        ip_addresses.append({'ip':addr.group(1),'port':port.group(1),'address': v['address'] })
        
for ip in ip_addresses:
    s = socket.socket()
    s.settimeout(1)
    port = 2154
    try:
        start = time.perf_counter()
        s.connect((ip['ip'], int(ip['port']))) 
       # print (ip['ip'], ' time taken ', time.perf_counter()-start ,' seconds')

    except Exception as e: 
        print(ip['address'])
    finally:
        s.close()
