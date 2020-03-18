#!/usr/bin/env python3

################################################################################
#
# Title:	01_get_cluster_details.py
# Author:	Adrian Bronder
# Date:		2020-17-03
# Description:	Get cluster information
#		with ONTAP Python client library
#
# Resources:	netapp_ontap.resources.cluster
#		netapp_ontap.resources.node
#		netapp_ontap.resources.aggregate
#		netapp_ontap.resources.port
#		
# URLs:		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://library.netapp.com/ecmdocs/ECMLP2858435/html/index.html
#
################################################################################

import json, os, sys
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Cluster, Node, Aggregate, Port


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
# Cluster
cluster = Cluster()
cluster.get()
print("--> Printing cluster details"
	+ "Name:    %s\n" % (cluster.name)
	+ "IP:      %s\n" % (cluster.management_interfaces[0].ip.address)
	+ "Version: %s\n" % (cluster.version.full)
)

# Nodes
print("--> Printing node details")
print("{:<20}{:<15}{:<15}{:<15}{:<10}".format(
        "Name", "Node", "Size", "Used", "State")
)
for node in Node.get_collection():
        node.get()
        print("{:<20}{:<15}{:<10}".format(
                node.name,
		node.serial_number,
                node.model
        ))
print("")

# Aggregates
print("--> Printing aggregate details")
print("{:<20}{:<15}{:<15}{:<15}{:<10}".format(
	"Name", "Node", "Size", "Used", "State")
)
for aggr in Aggregate.get_collection():
	aggr.get()
	print("{:<20}{:<15}{:<15}{:<15}{:<10}".format(
		aggr.name,
		aggr.home_node.name,
		aggr.space.block_storage.size,
		aggr.space.block_storage.used,
		aggr.state
	))
print("")

# Ports
print("--> Printing port details")
print("{:<10}{:<15}{:<10}{:<10}{:<10}{:<15}".format(
	"Name", "Node", "Speed", "MTU", "State", "BC Domain")
)
for port in Port.get_collection():
	port.get()
	print("{:<10}{:<15}{:<10}{:<10}{:<10}{:<15}".format(
		port.name,
		port.node.name,
		port.speed,
		port.mtu,
		port.state,
		port.broadcast_domain.name
	))
print("")
