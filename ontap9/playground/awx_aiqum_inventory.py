#!/usr/bin/env python3

################################################################################
#
# Title:        awx_aiqum_inventory
# Author:       Adrian Bronder
# Date:         2020-09-07
# Description:  Custom script for inventory collection with AWX from AIQUM
# Sources:	https://www.opcito.com/blogs/custom-inventory-management-using-ansible-awx-tower
#               with Ansible modulesdd
#
################################################################################

import os
import sys
import argparse
import requests

try:
        import json
except ImportError:
        import simplejson as json

class ExampleInventory(object):

        def __init__(self):
                self.inventory = {}
                self.read_cli_args()

                # Called with `--list`.
                if self.args.list:
                        self.inventory = self.example_inventory()
                # Called with `--host [hostname]`.
                elif self.args.host:
                        # Not implemented, since we return _meta info `--list`.
                        self.inventory = self.empty_inventory()
                # If no groups or vars are present, return an empty inventory.
                else:
                        self.inventory = self.empty_inventory()

                print(json.dumps(self.inventory));

        # Example inventory for testing.
        def example_inventory(self):
                headers = {
                        "accept": "application/json",
                        "authorization": "Basic YWRtaW46TmV0YXBwMSE=",
                        "UM-CSRF-Token": "c99d971e-909a-401f-9750-43e46ea80dfe"
                }
                url = "https://{}/api/datacenter/cluster/clusters".format("aiqum.demo.netapp.com")
                try:
                        response = requests.get(url, headers=headers, verify=False)
                except requests.exceptions.HTTPError as err:
                        print(err)
                        sys.exit(1)
                except requests.exceptions.RequestException as err:
                        print(err)
                        sys.exit(1)
                tmp = dict(response.json())
                clusters = tmp['records']

                inv_clusters = {
                        'ontap_clusters': {
                                'hosts': [],
                                'vars': {}
                        },
                        '_meta': {
                                'hostvars': {}
                        }
                }
#                print(inv_clusters)
                for cluster in clusters:
                        inv_clusters["ontap_clusters"]["hosts"].append(cluster["management_ip"])

                return inv_clusters

#               print("NOW I WANT TO LIST CLUSTERS")
#               print(inv_clusters)
#
#               return {
#                       'group': {
#                               'hosts': ['192.168.0.101', '192.168.0.102'],
#                               'vars': {}
#                       },
#                       '_meta': {
#                               'hostvars': {
#                                       '192.168.0.101': {
#                                               'host_specific_var': 'foo'
#                                       },
#                                       '192.168.0.102': {
#                                               'host_specific_var': 'bar'
#                                       }
#                               }
#                       }
#               }

        # Empty inventory for testing.
        def empty_inventory(self):
                return {'_meta': {'hostvars': {}}}

        # Read the command line args passed to the script.
        def read_cli_args(self):
                parser = argparse.ArgumentParser()
                parser.add_argument('--list', action = 'store_true')
                parser.add_argument('--host', action = 'store')
                self.args = parser.parse_args()

# Get the inventory.
ExampleInventory()
