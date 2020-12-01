#!/usr/bin/env python3

################################################################################
#
# Title:	90_delete_all.py
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

def get_quota_bytes(quota):
	return int(quota) * (1000 ** 3)

def get_info(endpoint, auth_token):
	return requests.get(endpoint,
					headers={'accept': 'application/json', 'authorization': 'Bearer {}'.format(auth_token)},
					verify=False).json()['data']

def tenant_exists(tenant_name, tenant_list):
	tenants = 0
	for x in tenant_list:
		if x['name'] == tenant_name:
			tenants += 1

	if tenants == 0:
		return False
	else:
		return True

def get_id(element, element_list):
	elements = []
	for x in element_list:
		if 'displayName' in x:
			if x['displayName'] == element:
				elements.append(x)
		else:
			if x['name'] == element:
				elements.append(x)

	if len(elements) == 0:
		print('Element {} does not exist.'.format(element))
		exit()
	elif len(elements) > 1:
		print('There is more than one Element with the name {}.'.format(element))
		exit()
	else:
		return elements[0]['id']


### Step 1 - Read in global variables
with open(os.path.dirname(sys.argv[0])+'../global.vars') as json_file:
	global_vars = json.load(json_file)


### Step 2 - Set Authorization Header
grid_auth_body = {
        "username":         global_vars['SG_ADMIN_USER'],
        "password":   		global_vars['SG_ADMIN_PASS'],
        "cookie":           "false",
        "csrfToken":   		"false"
      	}

### Step 3 - Get Grid Authorization Token
grid_auth = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/authorize',
                    data=json.dumps(grid_auth_body),
                    headers={'Content-Type':'application/json', 'accept':'application/json'},
					verify=False).json()['data']


### Step 4 - Get Tenent Authorization Token
tenant_id = get_id(global_vars['TENANT'], get_info(_url('/grid/accounts'), grid_auth))

tenant_auth_body = {
		"accountId":		tenant_id,
		"username": 		"root",
		"password": 		global_vars['TENANT_ROOT_PASS'],
		"cookie": 			"true",
		"csrfToken": 		"false"
		}

tenant_auth = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/authorize',
                    data=json.dumps(tenant_auth_body),
                    headers={'Content-Type':'application/json', 'accept':'application/json'},
					verify=False).json()['data']


### Step 5 - Delete Buckets
bucket_list = get_info(_url('/org/containers'), tenant_auth)

for bucket in bucket_list:
	bucket_del_resp = requests.delete('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/org/containers/{}'.format(bucket['name']),
				headers={'Content-Type':'application/json', 'accept':'application/json', 'authorization': 'Bearer {}'.format(tenant_auth)},
				verify=False)

	if bucket_del_resp.status_code == 204:
		print('Bucket {} deleted'.format(bucket['name']))
	else:
		print('\nError: {0} - {1}\n'.format(bucket_del_resp['code'], bucket_del_resp['message']['text']))


### Step 6 - Delete Tenant
tenant_del_resp = requests.delete('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/grid/accounts/{}'.format(tenant_id),
                    headers={'Content-Type':'application/json', 'accept':'application/json', 'authorization': 'Bearer {}'.format(grid_auth)},
					verify=False)

if tenant_del_resp.status_code == 204:
	print('Tenant {} deleted'.format(global_vars['TENANT']))
else:
	print('\nError: {0} - {1}\n'.format(tenant_del_resp['code'], tenant_del_resp['message']['text']))
