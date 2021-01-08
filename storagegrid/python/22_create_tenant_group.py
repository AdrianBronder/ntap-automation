#!/usr/bin/env python3

################################################################################
#
# Title:	22_create_tenant_group.py
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
with open(os.path.dirname(sys.argv[0])+'/../global.vars') as json_file:
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


### Step 5 - Create Tenant Group
tenant_group_body = {
		"displayName": 		global_vars["TENANT_GROUP_NAME"],
		"policies": {
			"management": {
				"manageAllContainers": True,
				"manageEndpoints": True,
				"manageOwnS3Credentials": False,
				"rootAccess": False
			},
			"s3": {
				"Statement": [
					{
					"Effect": "Allow",
					"Action": "s3:*",
					"Resource": [
						"arn:aws:s3:::*"
					],
					}
				]
			},
		},
		"uniqueName": "group/{}".format(global_vars["TENANT_GROUP_NAME"])
		}

group_create_resp = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/org/groups',
				data=json.dumps(tenant_group_body),
				headers={'Content-Type':'application/json', 'accept':'application/json', 'authorization': 'Bearer {}'.format(tenant_auth)},
				verify=False).json()


### Step 6 - Print Results
if group_create_resp['code'] == 201:
	print('\nTenant Group {0} created successfully.'.format(global_vars['TENANT_GROUP_NAME']))
else:
	print('Error: {0} - {1}'.format(group_create_resp['code'], group_create_resp['message']['text']))



