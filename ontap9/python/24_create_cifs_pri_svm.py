#!/usr/bin/env python3

################################################################################
#
# Title:	24_create_cifs_pri_svm.py
# Author:	Adrian Bronder
# Date:		2020-17-03
# Description:	Create CIFS server on primary SVM
#		with ONTAP Python client library
#
# Resources:    netapp_ontap.resources.cifs_service
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import CifsService


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


### Step 3 - Create operation
cifs = CifsService.from_dict(
{
  "name": global_vars["PRI_SVM"],
  "svm": {
    "name": global_vars["PRI_SVM"]
  },
  "ad_domain": {
    "fqdn": global_vars["PRI_AD_DOMAIN"],
    "user": global_vars["PRI_AD_USER"],
    "password": global_vars["PRI_AD_PASS"]
  },
  "comment": "Created with ONTAP PCL"
})

print("--> Starting CIFS create operation")
try:
	cifs.post()
	print("--> CIFS Server \"{}\" created successfully".format(cifs.name))
except NetAppRestError as err:
	print("--> Error: SVM was not created:\n{}".format(err))
print("")
