#!/usr/bin/env python3

################################################################################
#
# Title:	12_create_dns_pri_svm.py
# Author:	Adrian Bronder
# Date:		2020-17-03
# Description:	Create DNS entries on primary SVM
#		with ONTAP Python client library
#
# Resources:    netapp_ontap.resources.dns
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Dns


### Step 1 - Read in global variables
with open('../global.vars') as json_file:
	global_vars = json.load(json_file)


### Step 2 - Configure connection
config.CONNECTION = HostConnection(
	global_vars["PRI_CLU"],
	username=global_vars["PRI_CLU_USER"],
	password=global_vars["PRI_CLU_PASS"],
	verify=False
)


### Step 3 - Create management interface for SVM
dns = Dns.from_dict(
{
  "svm": {
    "name": global_vars["PRI_SVM"]
  },
  "domains": [
    global_vars["PRI_DOMAIN"]
  ],
  "servers": [
    global_vars["PRI_DNS1"]
  ]
})

print("--> Starting DNS create operation")
try:
	dns.post()
	print("--> DNS created successfully on SVM {}".format(dns.svm.name))
except NetAppRestError as err:
	print("--> Error: SVM was not created:\n{}".format(err))
print("")
