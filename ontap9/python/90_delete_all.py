#!/usr/bin/env python3

################################################################################
#
# Title:	90_delete_all.py
# Author:	Adrian Bronder
# Date:		2020-17-03
# Description:	Clean up the entire environment
#		with ONTAP Python client library
#
# Resources:	netapp_ontap.resources.volume
#		netapp_ontap.resources.cifs_service
#		netapp_ontap.resources.svm
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys, logging
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Volume, CifsService, Svm


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


### Step 3 - Delete operation
# Volume
print("--> Starting volume delete operation")
try:
	for volume in Volume.get_collection(
		**{"svm.name":global_vars["PRI_SVM"], "name":"!*_root"}):
		volume.delete()
		print("--> Volume {} deleted successfully".format(volume.name))
except NetAppRestError as err:
	print("--> Error: Volume was not deleted:\n{}".format(err))
print("")

# CIFS Server
print("--> Starting CIFS server delete operation")
try:
	cifs = CifsService.find(name=global_vars["PRI_SVM"])
	if cifs:
		cifs.delete(body={
			"ad_domain": {
				"fqdn": global_vars["PRI_AD_DOMAIN"],
				"user": global_vars["PRI_AD_USER"], 
				"password": global_vars["PRI_AD_PASS"]
			}
		})
		print("--> CIFS server {} deleted successfully".format(cifs.name))
except NetAppRestError as err:
	print("--> Error: CIFS server was not deleted:\n{}".format(err))
print("")

# SVM
print("--> Starting SVM delete operation")
try:
	svm = Svm.find(**{"name": global_vars["PRI_SVM"]})
	if svm:
		svm.delete()
		print("--> SVM {} deleted successfully".format(svm.name))
except NetAppRestError as err:
	print("--> Error: SVM was not deleted:\n{}".format(err))
print("")
