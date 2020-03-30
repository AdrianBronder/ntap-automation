#!/usr/bin/env python3

################################################################################
#
# Title:	26_create_nfs_pri_svm.py
# Author:	Adrian Bronder
# Date:		2020-17-03
# Description:	Create NFS server on primary SVM
#		with ONTAP Python client library
#
# Resources:    netapp_ontap.resources.nfs_service
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import NfsService


### Step 1 - Read in global variables
with open(os.path.dirname(sys.argv[0])+'/../global.vars') as json_file:
	global_vars = json.load(json_file)


### Step 2 - Configure connection
config.CONNECTION = HostConnection(
	global_vars["PRI_CLU"],
	username=global_vars["PRI_CLU_USER"],
	password=global_vars["PRI_CLU_PASS"],
	verify=False
)


### Step 3 - Create operation
nfs = NfsService.from_dict(
{
  "svm": {
    "name": global_vars["PRI_SVM"]
  },
  "enabled": "true",
  "protocol": {
    "v3_enabled": "true",
    "v40_enabled": "false",
    "v41_enabled": "false"
  }
})

print("--> Starting interface create operation")
try:
	nfs.post()
	print("--> NFS server created successfully on SVM \"{}\"".format(nfs.svm.name))
except NetAppRestError as err:
	print("--> Error: SVM was not created:\n{}".format(err))
print("")
