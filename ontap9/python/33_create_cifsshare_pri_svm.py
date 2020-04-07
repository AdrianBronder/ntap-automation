#!/usr/bin/env python3

################################################################################
#
# Title:	33_create_cifsshare_pri_svm.py
# Author:	Adrian Bronder
# Date:		2020-03-17
# Description:	Create CIFS share on primary SVM
#		with ONTAP Python client library
#
# Resources:    netapp_ontap.resources.cifs_share
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import CifsShare


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
cifsshare = CifsShare.from_dict(
{
  "name": "share_01",
  "svm": {
    "name": global_vars["PRI_SVM"]
  },
  "path": "/"+global_vars["PRI_SVM"]+"_cifs_01/cifs_01/"
})

print("--> Starting CIFS share create operation")
try:
	cifsshare.post()
	print("--> CIFS share \"{}\" created successfully".format(cifsshare.name))
except NetAppRestError as err:
	print("--> Error: SVM was not created:\n{}".format(err))
print("")
