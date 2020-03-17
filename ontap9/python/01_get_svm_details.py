#!/usr/bin/env python3

################################################################################
#
# Title:	01_get_svm_details.py
# Author:	Adrian Bronder
# Date:		2020-17-03
# Description:	Get SVM information
#		with ONTAP Python client library
#
# Resources:    netapp_ontap.resources.svm
#		netapp_ontap.resources.ip_interface
#               netapp_ontap.resources.dns
#               netapp_ontap.resources.cifs_service
#               netapp_ontap.resources.nfs_service
#
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Svm, IpInterface, Dns, CifsService, NfsService


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


### Step 3 - Get & print SVM details
# SVMs
print("--> Printing SVM details")
print("{:<20}{:<15}{:<10}{:<30}".format(
	"Name", "IP Space", "State", "Comment")
)
for svm in Svm.get_collection():
	svm.get()
	print("{:<20}{:<15}{:<10}{:<30}".format(
		svm.name,
		svm.ipspace.name,
		svm.state,
		svm.comment
        ))
print("")

# Interfaces
print("--> Printing network interface details")
print("{:<20}{:<25}{:<20}{:<15}".format(
	 "SVM", "Name", "IP", "Current Port")
)
for lif in IpInterface.get_collection(**{"scope": "svm"}):
        lif.get()
        print("{:<20}{:<25}{:<20}{:15}".format(
                lif.svm.name,
		lif.name,
		lif.ip.address+"/"+lif.ip.netmask,
		lif.location.node.name+":"+lif.location.port.name
        ))
print("")

# DNS
print("--> Printing DNS details")
print("{:<20}{:<20}{:<20}".format(
	"SVM", "Domains", "Servers")
)
for dns in Dns.get_collection():
	dns.get()
	print("{:<20}{:<20}{:<20}".format(
		dns.svm.name,
		str(dns.domains),
		str(dns.servers)
	))
print("")

# CIFS
print("--> Printing CIFS details")
print("{:<20}{:<20}{:<20}{:<20}".format(
	"SVM", "Server Name", "Domain", "Comment")
)
for cifs in CifsService.get_collection():
	cifs.get()
	print("{:<20}{:<20}{:<20}{:<20}".format(
		cifs.svm.name,
		cifs.name,
		cifs.ad_domain.fqdn,
		cifs.comment
	))
print("")

# CIFS
print("--> Printing CIFS details")
print("{:<20}{:<10}{:<10}{:<10}{:<10}".format(
        "SVM", "State", "v3", "v4.0", "v4.1")
)
for nfs in NfsService.get_collection():
	nfs.get()
	print("{:<20}{:<10}{:<10}{:<10}{:<10}".format(
		nfs.svm.name,
		nfs.state,
		str(nfs.protocol.v3_enabled),
		str(nfs.protocol.v40_enabled),
		str(nfs.protocol.v41_enabled)
	))
print("")
