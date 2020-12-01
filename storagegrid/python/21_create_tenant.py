#!/usr/bin/env python3

################################################################################
#
# Title:	21_create_tenant.py
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

### Step 4 - Check if Tenant already exists
if tenant_exists(global_vars['TENANT'], get_info(_url('/grid/accounts'), grid_auth)):
	print('A tenant with the name {} already exists.'.format(global_vars['TENANT']))
	exit()

### Step 5 - Create Tenant
tenant_create_data = {
		"name": 			global_vars['TENANT'],
		"capabilities": [
			"management",
			"s3"
		],
		"policy": {
			"useAccountIdentitySource": 	True,
			"allowPlatformServices": 		False,
			"quotaObjectBytes": 			get_quota_bytes(global_vars['DEFAULT_QUOTA'])
		},
		"password": 		global_vars['TENANT_ROOT_PASS']
		}

tenant_create_resp = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/grid/accounts',
                    data=json.dumps(tenant_create_data),
                    headers={'Content-Type':'application/json', 'accept':'application/json', 'authorization': 'Bearer {}'.format(grid_auth)},
					verify=False).json()

### Step 5 - Print confirmation
if tenant_create_resp['code'] == 201:
	print('Status: {0:15}'.format(tenant_create_resp['status']))
	print('\nTenant {0} with ID: {1} created.'.format(global_vars['TENANT'], tenant_create_resp['data']['id']))
else:
	print('Creation not successful.')
	print('\nCode: {0:15}   Status: {1:20}'.format(tenant_create_resp['code'], tenant_create_resp['status'] ))




