#!/usr/bin/env python3

################################################################################
#
# Title:	03_get_filesystem_details.py
# Author:	Adrian Bronder
# Date:		2020-17-03
# Description:	Get filesystem information
#		with ONTAP Python client library
#
# Resources:    netapp_ontap.resources.volume
#		netapp_ontap.resources.qtree
#               netapp_ontap.resources.cifs_sahre
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Volume, Qtree, CifsShare


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


### Step 3 - Get & print details
# Volumes
print("--> Printing volume details")
print("{:<20}{:<25}{:<15}{:<15}".format(
	"SVM", "Name", "Size", "Used")
)
for volume in Volume.get_collection():
	volume.get()
	print("{:<20}{:<25}{:<15}{:<15}".format(
		volume.svm.name,
		volume.name,
		volume.size,
		volume.space.used
	))
print("")

# Qtrees
print("--> Printing qtree details")
print("{:<20}{:<10}{:<15}{:<35}".format(
	 "SVM", "Style", "Export Policy", "Path")
)
for qtree in Qtree.get_collection():
        qtree.get()
        print("{:<20}{:<10}{:<15}{:<35}".format(
                qtree.svm.name,
		qtree.security_style,
		qtree.export_policy.name,
		qtree.path
        ))
print("")

# CIFS Shares
print("--> Printing CIFS share details")
print("{:<20}{:<15}{:<35}".format(
	"SVM", "Share", "Path")
)
for cifsshare in CifsShare.get_collection():
	cifsshare.get()
	print("{:<20}{:<15}{:<35}".format(
		cifsshare.svm.name,
		cifsshare.name,
		cifsshare.path
	))
print("")
