#!/usr/bin/env python3

################################################################################
#
# Title:	36_create_nfsvol_pri_svm.py
# Author:	Adrian Bronder
# Date:		2020-03-17
# Description:	Create volume on primary SVM
#		with ONTAP Python client library
#
# Resources:    netapp_ontap.resources.volume
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Volume


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
# execute create operation
volume = Volume.from_dict(
{
  "name": global_vars["PRI_SVM"]+"_nfs_01",
  "svm": {
    "name": global_vars["PRI_SVM"]
  },
  "size": global_vars["VOL_SIZE"],
  "aggregates": [
    {
      "name": global_vars["PRI_AGGR"]
    }
  ],
  "comment": "Created with ONTAP PCL",
  "guarantee": {
    "type": "volume"
  },
  "nas": {
    "export_policy": {
      "name": "default"
    },
    "path": "/"+global_vars["PRI_SVM"]+"_nfs_01",
    "security_style": "unix"
  }
})

print("--> Starting volume create operation")
try:
	volume.post()
	print("--> Volume \"{}\" created successfully".format(volume.name))
except NetAppRestError as err:
	print("--> Error: SVM was not created:\n{}".format(err))
print("")
