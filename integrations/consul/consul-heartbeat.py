#!/usr/bin/env python

from alertaclient.api import ApiClient
from alertaclient.alert import Alert
from alertaclient.heartbeat import Heartbeat
import sys
import os
import time
import json
import consul
import time

client = consul.Consul(host='127.0.0.1', port=8500, token=None, scheme='http', consistency='default', dc=None, verify=True)

url = client.kv.get('alerta/apiurl')[1]['Value']
key = client.kv.get('alerta/apikey')[1]['Value']

max_retries = int(client.kv.get('alerta/max_retries')[1]['Value'])
sleep = int(client.kv.get('alerta/sleep')[1]['Value'])
timeout = int(client.kv.get('alerta/timeout')[1]['Value'])

origin = client.kv.get('alerta/origin')[1]['Value']
api = ApiClient(endpoint=url, key=key)

def createheartbeat():
    hb = Heartbeat(origin=origin, timeout=timeout)
    for i in range(max_retries):
        try:
            print(api.send(hb))
        except Exception as e:
            print("HTTP Error: {}".format(e))
            time.sleep(sleep)
            continue
        else:
            break
    else:
        print("api is down")

def main():
    createheartbeat()

if __name__ == "__main__":
    main()
