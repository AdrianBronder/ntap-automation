#!/usr/bin/env python3

################################################################################
#
# Title:	32_create_cifsqtree_pri_svm.py
# Author:	Adrian Bronder
# Date:		2020-17-03
# Description:	Create qtree on primary SVM
#		with ONTAP Python client library
#
# Resources:    netapp_ontap.resources.qtree
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree


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
# execute create operation
qtree = Qtree.from_dict(
{
  "name": "cifs_01",
  "svm": {
    "name": global_vars["PRI_SVM"]
  },
  "volume": {
    "name": global_vars["PRI_SVM"]+"_cifs_01"
  },
  "security_style": "ntfs"
}
)

print("--> Starting qtree create operation")
try:
	qtree.post()
	print("--> Qtree \"{}\" created successfully".format(qtree.name))
except NetAppRestError as err:
	print("--> Error: SVM was not created:\n{}".format(err))
print("")
