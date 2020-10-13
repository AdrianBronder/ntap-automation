#!/usr/bin/env bash

################################################################################
#
# Title:	sl10599_init_cluster.sh
# Author:	Adrian Bronder
# Date:		2020-09-03
# Description:	Prepare primary storage cluster "cluster1" in LoD lab sl10599
#		--> "Exploring the ONTAP REST API v1.2"
#
# URLs:		https://labondemand.netapp.com/lab/sl10599
#		http://docs.netapp.com/ontap-9/index.jsp
#		https://pypi.org/project/netapp-ontap/
#		https://galaxy.ansible.com/netapp/ontap
#
################################################################################


### Step 1 - Get list of aggregates and available spares from cluster"

REST_RESPONSE=`curl -s \
  -H "accept: application/hal+json"\
  -H "authorization: Basic YWRtaW46TmV0YXBwMSE="\
  -X GET\
  "https://cluster1.demo.netapp.com/api/storage/aggregates?show_spares=true"`


### STEP 2 - Create aggreagets, if spare count is sufficient

if [[ `echo $REST_RESPONSE | jq -r '.spares | length'` -gt 0 ]]; then
  echo $REST_RESPONSE | jq -r '.spares[] | [.node.name, .usable] | @tsv' |
    while IFS=$'\t' read -r NODE SPARES; do
      if [[ $SPARES -gt 5 ]]; then
	echo "--> Creating aggr with $(($SPARES)) disks on node $NODE"
        POST_DATA=`cat <<EOF
{
  "name": "aggr1_$(echo $NODE | tr '-' '_')",
  "node": {
    "name": "$NODE"
  },
  "block_storage": {
    "primary": {
      "disk_count": $(($SPARES))
    }
  }
}
EOF`
        curl -s \
          -H "accept: application/hal+json" \
          -H "authorization: Basic YWRtaW46TmV0YXBwMSE=" \
          -X POST \
          "https://cluster1.demo.netapp.com/api/storage/aggregates" \
          -d "$POST_DATA"
      fi
    done
else
  echo "No spares found. Skipping creation of aggreagets."
fi
