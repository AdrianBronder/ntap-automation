#!/usr/bin/env python3

################################################################################
#
# Title:        awx_ci_inventory
# Author:       Adrian Bronder
# Date:         2020-10-01
# Description:  Custom script for inventory collection with AWX from Cloud Insights
#               with Ansible modules
#
# Sources:      https://www.opcito.com/blogs/custom-inventory-management-using-ansible-awx-tower
#
# Notice:       Requires custom credential type to add "ci_tenant_url" and
#               "ci_access_token" to environment variables
#
################################################################################

import os
import sys
import argparse
import requests
import base64

#os.environ["ci_tenant_url"]=''
#os.environ["ci_access_token"]=''

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
                        "X-CloudInsights-ApiKey": os.environ.get("ci_access_token")
                }
                url = "{}/rest/v1/assets/storages".format(os.environ.get("ci_tenant_url"))
                try:
                        response = requests.get(url, headers=headers, verify=False)
                except requests.exceptions.HTTPError as err:
                        print(err)
                        sys.exit(1)
                except requests.exceptions.RequestException as err:
                        print(err)
                        sys.exit(1)
                clusters = response.json()

                inv_clusters = {
                        'ontap_clusters': {
                                'hosts': [],
                                'vars': {}
                        },
                        '_meta': {
                                'hostvars': {}
                        }
                }

                for cluster in clusters:
                        inv_clusters["ontap_clusters"]["hosts"].append(cluster["ip"])

                return inv_clusters

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
