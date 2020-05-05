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
#$REST_RESPONSE | ConvertTo-Json

$ntap_cluster = New-Object -TypeName psobject
$ntap_cluster | Add-Member -MemberType NoteProperty -Name "Name" -Value $REST_RESPONSE.name
$ntap_cluster | Add-Member -MemberType NoteProperty -Name "IP" -Value $REST_RESPONSE.management_interfaces[0].ip.address
$ntap_cluster | Add-Member -MemberType NoteProperty -Name "Version" -Value $REST_RESPONSE.version.full

Write-Host "--> Printing cluster details"
($ntap_cluster | Format-List | Out-String).Trim()
Write-Host ""

# Nodes
$API="https://$($GLOBAL_VARS.PRI_CLU)/api/cluster/nodes?fields=*"
Write-Host "--> calling $API"
$REST_RESPONSE = Invoke-RestMethod -Uri $API -Headers $hdrs -Method GET

Write-Host "--> Printing node details"
($REST_RESPONSE.records | Select-Object name, serial_number, model | Out-String).Trim()



#$ntap_nodes = New-Object System.Collections.ArrayList
#foreach($node in $REST_RESPONSE.records){
#    $temp = "" | select "Name", "serial_number", "Model"
#    $temp.Name = $node.name
#    $temp.serial_number = $node.serial_number
#    $temp.Model = $node.model
#    $ntap_nodes.Add($temp) | Out-Null
#}
#$ntap_nodes