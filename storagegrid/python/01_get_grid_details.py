#!/usr/bin/env python3

################################################################################
#
# Title:	01_get_grid_details.py
# Author:	Adrian Bronder
# Date:		2020-03-17
# Description:	Get grid information
#
# Resources:	
#		
# URLs:	
#
################################################################################

import json, os, sys
import requests

### Define Functions
def _url(path):
	return 'https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3' + path

def get_info(endpoint, auth_token):
	return requests.get(endpoint,
					headers={'accept': 'application/json', 'authorization': 'Bearer {}'.format(auth_token)},
					verify=False).json()['data']

### Step 1 - Read in global variables
with open(os.path.dirname(sys.argv[0])+'../global.vars') as json_file:
	global_vars = json.load(json_file)

api_requests = ['/grid/config/product-version', 'grid/health/topology']

### Step 2 - Set Authorization Header
auth_body = {
        "username":            global_vars['SG_ADMIN_USER'],
        "password":            global_vars['SG_ADMIN_PASS'],
        "cookie":              "false",
        "csrfToken":           "false"
      	}

### Step 3 - Get Grid Authorization Token
grid_auth = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/authorize',
                    data=json.dumps(auth_body),
                    headers={'Content-Type':'application/json', 'accept':'application/json'},
					verify=False).json()['data']

### Step 4 - Get Grid Info - Version & Topology
version_resp = get_info(_url('/grid/config/product-version'), grid_auth)
topology_resp = get_info(_url('/grid/health/topology'), grid_auth)

### Step 5 - Print Info
print('\n{0:13}{1}'.format('Name:', topology_resp['name']))
print('{0:13}{1}\n'.format('Version:', version_resp['productVersion']))

for site in topology_resp['children']:
	print('Data Center: {}'.format(site['name']))
	for node in site['children']:	
		print(' - Node Name: {0:20} 	Type: {1}'.format(node['name'], node['type']))
	print('\n')


