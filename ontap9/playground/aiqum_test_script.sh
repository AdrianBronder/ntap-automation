#!/usr/bin/env bash

HEAD_APP="content-type: application/hal+json"

API="http://rhel1.demo.netapp.com/api/v2/job_templates/read_info/launch/"

REST_RESPONSE=`curl -s\
    -H "$HEAD_APP" -u "admin:Netapp1!" -X POST "$API"`
