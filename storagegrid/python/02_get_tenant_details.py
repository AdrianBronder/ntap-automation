#!/usr/bin/env python3

################################################################################
#
# Title:	02_get_tenant_details.py
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

def get_tenant_details(tenant_name, tenant_list):
	tenants = []
	for x in tenant_list:
		if x['name'] == tenant_name:
			tenants.append(x)

	if len(tenants) == 0:
		print('Tenant {} does not exist.'.format(global_vars['TENANT']))
		exit()
	elif len(tenants) > 1:
		print('There is more than one tenant with the name {}.'.format(global_vars['TENANT']))
		exit()
	else:
		return tenants[0]

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

### Step 4 - Get Tenent Info - Config & Usage
tenant_details = get_tenant_details(global_vars['TENANT'], get_info(_url('/grid/accounts'), grid_auth))
tenant_usage = get_info(_url('/grid/accounts/{}/usage'.format(tenant_details['id'])), grid_auth)

### Step 5 - Print Info
print('\n{0:15}{1}'.format('Tenant:', tenant_details['name']))
print('{0:15}{1}\n'.format('ID:', tenant_details['id']))
print('{0:15}{1}\n'.format('Capabilities:', tenant_details['capabilities']))
print('{0:15}{1:25}{2}'.format('Policy:', 'Allow Platform Services:', tenant_details['policy']['allowPlatformServices']))
print('{0:15}{1:25}{2}'.format('', 'Use Identity Source:', tenant_details['policy']['useAccountIdentitySource']))
print('{0:15}{1:25}{2} GB'.format('', 'Quota:', int(tenant_details['policy']['quotaObjectBytes'] / (1000 ** 3)) ))
print('\n{0:15}{1:25}{2} GB'.format('', 'Usage:', int(tenant_usage['dataBytes'] / (1000 ** 3)) ))
print('\n')




