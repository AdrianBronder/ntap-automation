#!/usr/bin/env python3

################################################################################
#
# Title:	23_create_tenant_user.py
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

group_id = get_id(global_vars['TENANT_GROUP_NAME'], get_info(_url('/org/groups'), tenant_auth))

tenant_user_body = {
		"fullName": 		global_vars['TENANT_USER_NAME'],
		"memberOf": [
			"{}".format(group_id)
		],
		"disable": False,
		"uniqueName": "user/{}".format(global_vars["TENANT_USER_NAME"])
		}

### Step 5 - 
user_create_resp = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/org/users',
				data=json.dumps(tenant_user_body),
				headers={'Content-Type':'application/json', 'accept':'application/json', 'authorization': 'Bearer {}'.format(tenant_auth)},
				verify=False).json()
if user_create_resp['code'] == 201:
	print('\nTenant User {0} as member of {1} created successfully.\n'.format(global_vars['TENANT_USER_NAME'], global_vars['TENANT_GROUP_NAME']))
else:
	print('\nError: {0} - {1}\n'.format(user_create_resp['code'], user_create_resp['message']['text']))



