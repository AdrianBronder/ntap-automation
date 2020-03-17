#!/usr/bin/env python3

################################################################################
#
# Title:	14_create_nfslif_pri_svm.py
# Author:	Adrian Bronder
# Date:		2020-17-03
# Description:	Create an NFS interface on primary SVM
#		with ONTAP Python client library
#
# Resources:    netapp_ontap.resources.IpInterface
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import IpInterface


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
lif = IpInterface.from_dict(
{
  "name": global_vars["PRI_SVM"]+"_nfs_01",
  "svm": {
    "name": global_vars["PRI_SVM"]
  },
  "ip": {
    "address": global_vars["PRI_SVM_NFS_IP"],
    "netmask": global_vars["PRI_SVM_NFS_NETMASK"]
  },
  "location": {
    "home_port": {
      "name": global_vars["PRI_DATA_PORT"],
      "node": {
        "name": global_vars["PRI_NODE"]
      }
    }
  },
  "service_policy": {
    "name": "default-data-files"
  }
})

print("--> Starting interface create operation")
try:
	lif.post()
	print("--> NFS interface \"{}\" created successfully".format(lif.name))
except NetAppRestError as err:
	print("--> Error: SVM was not created:\n{}".format(err))
print("")
