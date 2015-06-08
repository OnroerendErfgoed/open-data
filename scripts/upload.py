#!/usr/bin/env python

import requests
import pprint
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))

METADATA_DIR = os.path.join(HERE,'..','metadata')

API_KEY = IN_TE_VULLEN

HOST = 'http://ckan-001.corve.openminds.be'

BASE_URL = HOST + '/api/3/action'

pp = pprint.PrettyPrinter(indent=4)

s = requests.Session()
s.headers.update({
    'Authorization': API_KEY,
    'Content-Type': 'application/json'
})

def print_underlined(msg, underline_with='-'):
    print(msg)
    print(len(msg)*underline_with)

r = s.get(BASE_URL + '/organization_show', params={'id': 'onroerend-erfgoed'})

data = r.json()['result']

pp.pprint(data)

print_underlined(data['name'], underline_with='=')
print_underlined('users')
for u in data['users']:
    print('\t' + u['display_name'])
print_underlined('datasets')
for p in data['packages']:
    print('\t' + p['name'])

for root, dirs, files in os.walk(METADATA_DIR):
    if len(files) > 0:
        for name in files:
            print(os.path.join(root, name))
            with open(os.path.join(root, name)) as package:
                package = json.load(package)
                package_id = package['name']
            r = s.get(BASE_URL + '/package_show', params={'id': package_id})
            res = r.json()
            if res.get('success', False):
                print('Need to update %s' % res['result']['name'])
                r = s.post(BASE_URL + '/package_update', data=json.dumps(package))
                r.raise_for_status()
            else:
                print('Need to create %s' % package_id)
                r = s.post(BASE_URL + '/package_create', data=json.dumps(package))
                r.raise_for_status()
