#!/usr/bin/env python3

################################################################################
#
# Title:	24_create_s3credentials.py
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
		elif 'fullName' in x:
			if x['fullName'] == element:
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


### Step 5 - Get User ID 
user_id = get_id(global_vars['TENANT_USER_NAME'], get_info(_url('/org/users'), tenant_auth))


### Step 6 - Make sure S3 Creds Directory exists.
s3creds_dir = r'../cred_store/'
s3creds_filepath = '{0}{1}-{2}.txt'.format(s3creds_dir, global_vars['TENANT'], global_vars['TENANT_USER_NAME'])

if not os.path.exists(s3creds_dir):
    os.makedirs(s3creds_dir)


### Step 7 - Create S3 Credentials for User
s3creds_data = {
#		"expires": "2020-09-04T00:00:00.000Z"
		}

s3creds_resp = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3//org/users/{}/s3-access-keys'.format(user_id),
				data=json.dumps(s3creds_data),
				headers={'Content-Type':'application/json', 'accept':'application/json', 'authorization': 'Bearer {}'.format(tenant_auth)},
				verify=False).json()

### Step 8 - Print Status and save S3 Creds to file
if s3creds_resp['code'] == 201:
	with open(s3creds_filepath, 'w') as outfile:
		json.dump(s3creds_resp['data'], outfile)

	print('\nS3 Credentials for User {0} have been created successfully.\n'.format(global_vars['TENANT_USER_NAME']))
	print('S3 Access Key:{}'.format(s3creds_resp['data']['displayName']))
	print('S3 Credentials saved to: {}\n'.format(s3creds_filepath))
else:
	print('\nError: {0} - {1}\n'.format(user_create_resp['code'], user_create_resp['message']['text']))



