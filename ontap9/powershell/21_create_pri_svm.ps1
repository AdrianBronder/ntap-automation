#!/usr/bin/env pwsh

################################################################################
#
# Title:        21_create_pri_svm.ps1
# Author:       Adrian Bronder
# Date:         2020-05-05
# Description:  Create a primary SVM
#               with ONTAP Python client library
#
# APIs:         /api/svm/svms
#
# URLs:         http://docs.netapp.com/ontap-9/index.jsp
#               https://pypi.org/project/netapp-ontap/
#
################################################################################


### Step 1 - Read in global variables
$GLOBAL_VARS = Get-Content -Raw -Path $PSScriptRoot"\..\global.vars" | ConvertFrom-Json
### Step 1.5 ;-) - Allow self-signed certificates
. $PSScriptRoot\00_certs_and_protocols.ps1


### Step 2 - Create HTTP headers
$TOKEN = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes("admin:Netapp1!"))
$hdrs = @{}
$hdrs.Add("Accept","application/hal+json")
$hdrs.Add("Authorization", "Basic $TOKEN")



### Step 3 - Create opeartion
# execute create operation
$API = "https://$($GLOBAL_VARS.PRI_CLU)/api/svm/svms"
$POST_DATA = @{
  "name" = $GLOBAL_VARS.PRI_SVM
  "aggregates" = @(
    @{
      "name"= $GLOBAL_VARS.PRI_AGGR
    }
  )
  "comment"= "Created with PS REST"
}

$REST_RESPONSE = Invoke-RestMethod -Uri $API -Headers $hdrs -Body ($POST_DATA|ConvertTo-Json) -Method POST

$JOB_URL=$REST_RESPONSE.job._links.self.href
Write-Host "--> SVM create job was started here:`nhttps://$($GLOBAL_VARS.PRI_CLU)$JOB_URL"

$JOB_API="https://$($GLOBAL_VARS.PRI_CLU)/$JOB_URL"
$JOB_STATUS="running"
while(($JOB_STATUS -eq "running")){
    $JOB_RESPONSE = Invoke-RestMethod -Uri $JOB_API -Headers $hdrs -Method GET
    $JOB_STATUS = $JOB_RESPONSE.state
    Write-Host "Job in state: $JOB_STATUS"
    sleep 2
}