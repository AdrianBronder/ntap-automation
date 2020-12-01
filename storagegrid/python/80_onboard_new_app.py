#!/usr/bin/env python3

################################################################################
#
# Title:	80_onboard_new_app.py
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
with open(os.path.dirname(sys.argv[0])+'../new_app.vars') as json_file:
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


### Step 6 - Get Tenent Authorization Token
tenant_auth_body = {
		"accountId":		tenant_create_resp['data']['id'],
		"username": 		"root",
		"password": 		global_vars['TENANT_ROOT_PASS'],
		"cookie": 			"true",
		"csrfToken": 		"false"
		}

tenant_auth = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/authorize',
                    data=json.dumps(tenant_auth_body),
                    headers={'Content-Type':'application/json', 'accept':'application/json'},
					verify=False).json()['data']


### Step 7 - Create Tenant Group
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


if group_create_resp['code'] != 201:
	print('\nError: {0} - {1}\n'.format(group_create_resp['code'], group_create_resp['message']['text']))
	exit()


### Step 8 - Create Tenant User 
tenant_user_body = {
		"fullName": 		global_vars['TENANT_USER_NAME'],
		"memberOf": [
			"{}".format(group_create_resp['data']['id'])
		],
		"disable": False,
		"uniqueName": "user/{}".format(global_vars["TENANT_USER_NAME"])
		}

user_create_resp = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/org/users',
				data=json.dumps(tenant_user_body),
				headers={'Content-Type':'application/json', 'accept':'application/json', 'authorization': 'Bearer {}'.format(tenant_auth)},
				verify=False).json()

if user_create_resp['code'] != 201:
	print('\nError: {0} - {1}\n'.format(user_create_resp['code'], user_create_resp['message']['text']))
	exit()


### Step 9 - Make sure S3 Creds Directory exists.
s3creds_dir = r'../cred_store/'
s3creds_filepath = '{0}{1}-{2}.txt'.format(s3creds_dir, global_vars['TENANT'], global_vars['TENANT_USER_NAME'])

if not os.path.exists(s3creds_dir):
    os.makedirs(s3creds_dir)


### Step 10 - Create S3 Credentials for User
s3creds_data = {
#		"expires": "2020-09-04T00:00:00.000Z"
		}

s3creds_resp = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3//org/users/{}/s3-access-keys'.format(user_create_resp['data']['id']),
				data=json.dumps(s3creds_data),
				headers={'Content-Type':'application/json', 'accept':'application/json', 'authorization': 'Bearer {}'.format(tenant_auth)},
				verify=False).json()

if s3creds_resp['code'] == 201:
	with open(s3creds_filepath, 'w') as outfile:
		json.dump(s3creds_resp['data'], outfile)
else:
	print('\nError: {0} - {1}\n'.format(user_create_resp['code'], user_create_resp['message']['text']))


### Step 11 - Create Bucket
bucket_body = {
		"name": 			global_vars["BUCKET_NAME"]
		}

bucket_create_resp = requests.post('https://' + global_vars["SG_ADMIN_NODE"] + '/api/v3/org/containers',
				data=json.dumps(bucket_body),
				headers={'Content-Type':'application/json', 'accept':'application/json', 'authorization': 'Bearer {}'.format(tenant_auth)},
				verify=False).json()


### Step 6 - Print Results
print('\nOnboarding Complete:')
print('\n{0:20}{1} - ID: {2}'.format('Tenant:', tenant_create_resp['data']['name'], tenant_create_resp['data']['id']))
print('{0:20}{1}'.format('User:', user_create_resp['data']['fullName']))
print('{0:20}{1}'.format('Group:', group_create_resp['data']['displayName']))
print('{0:20}{1}'.format('Bucket:', bucket_create_resp['data']['name']))
print('\nS3 Credentials for User {0} have been created successfully.'.format(global_vars['TENANT_USER_NAME']))
print('{0:30}{1}'.format('S3 Access Key:', s3creds_resp['data']['displayName']))
print('{0:30}{1}\n'.format('S3 Credentials saved to:', s3creds_filepath))





