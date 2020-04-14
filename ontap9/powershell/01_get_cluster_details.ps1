#!/usr/bin/env pwsh

################################################################################
#
# Title:        01_get_cluster_details.ps1
# Author:       Adrian Bronder
# Date:         2020-04-14
# Description:  Get cluster information
#		        with PowerShell using REST method
#
# APIs:         /api/cluster
#               /api/cluster/nodes
#               /api/storage/aggregates
#               /api/network/ethernet/ports
#
# URLs:         https://docs.netapp.com/ontap-9/index.jsp
#               https://<cluster>/docs/api
#
# Sample REST call:
# Invoke-RestMethod -Method GET -Headers $hdrs -Uri "https://<cluster>/api/cluster"
#
################################################################################


### Step 1 - Read in global variables
$GLOBAL_VARS=Get-Content -Raw -Path $PSScriptRoot"\..\global.vars" | ConvertFrom-Json
### Step 1.5 ;-) - Allow self-signed certificates
. $PSScriptRoot\00_certs_and_protocols.ps1


### Step 2 - Create HTTP headers
$TOKEN=[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes("admin:Netapp1!"))
$hdrs = @{}
$hdrs.Add("Accept","application/hal+json")
$hdrs.Add("Authorization", "Basic $TOKEN")


### Step 3 - Get & print details 
# Cluster 
$API="https://$($GLOBAL_VARS.PRI_CLU)/api/cluster?fields=*"
Write-Host "--> calling $API"
$REST_RESPONSE = Invoke-RestMethod -Uri $API -Headers $hdrs -Method GET

Write-Host "--> Printing cluster details"
$REST_RESPONSE | Select-Object -Property Name, management_interfaces, version
