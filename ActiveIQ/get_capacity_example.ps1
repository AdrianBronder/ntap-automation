  
#!/usr/bin/env pwsh

################################################################################
#
# Title:        2020-07-06 Get AIQ Capacity.ps1
# Author:       Adrian Bronder
# Date:         2020-07-06
# Description:  Get global capacity details from Active IQ
#		        with PowerShell using REST method
#
# APIs:         /v1/tokens/accessToken
#               /v1/search/aggregate/level
#               /v2/capacity/summary/level/{level}/id/{id}
#               /v2/capacity/details/level/{level}/id/{id}
#               ​/v1​/capacity​/trend​/level​/{level}​/id​/{id}
#
# URLs:         https://mysupport.netapp.com/myautosupport/dist/index.html#/apiservices
#               https://mysupport.netapp.com/myautosupport/dist/index.html#/apidocs/serviceList
#
################################################################################

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ENDPOINT = "https://api.activeiq.netapp.com"


### Step 1 - Check Credentials
if ( -not (Test-Path .\tokens.json) ){
    @{"access_token"=""; "refresh_token"=""} | ConvertTo-Json | Out-File .\tokens.json
}
$TOKENS = Get-Content -Raw -Path .\tokens.json | ConvertFrom-Json

if ( [string]::IsNullOrEmpty($TOKENS.refresh_token) ){
    $TOKENS.refresh_token = Read-Host -Prompt "Enter your Active IQ API 'REFRESH' token: "
}


### Step 2 - Generate an access token
$API = $ENDPOINT+"/v1/tokens/accessToken"
$HEADERS = @{
    "accept" = "application/json"
    "Content-Type" = "application/json"
}
$POST_DATA = @{
    "refresh_token" = $TOKENS.refresh_token
}

$REST_RESPONSE = Invoke-RestMethod -Uri $API -Headers $HEADERS -Body ($POST_DATA|ConvertTo-Json) -Method POST
$TOKENS.access_token = $REST_RESPONSE.access_token
$TOKENS.refresh_token = $REST_RESPONSE.refresh_token

$TOKENS | ConvertTo-Json | Out-File .\tokens.json
$HEADERS.Add("authorizationToken", $TOKENS.access_token)


### Step 3 - Get search criteria
$SEARCH_CATEGORY = Read-Host -Prompt "Enter a search categorie ('customer', 'group'): "
$SEARCH_STRING = Read-Host -Prompt "What are you searching for? (enter a string to search for) "
$SEARCH_TYPE = Read-Host -Prompt "What type of information are you searching for? ('capacity', 'system') "
$SEARCH_DEPTH = Read-Host -Prompt "At which level? ('summary', 'details') "


### Step 4 - Get list of entities
switch($SEARCH_CATEGORY) {
    "customer" {
        $API = $ENDPOINT+"/v1/search/aggregate/level/customer?name="+$SEARCH_STRING
    }
    "group" {
        $API = $ENDPOINT+"/v1/search/aggregate/level/group?name="+$SEARCH_STRING
    }
    Default {
        Write-host "Invalid search category provided. Valid values are 'customer' and 'group'."
        exit
    }
}
$REST_SEARCH_RESPONSE = Invoke-RestMethod -Uri $API -Headers $HEADERS -Method GET
<# foreach ($AIQ_ENTITY in $REST_SEARCH_RESPONSE.results ) {
    Write-Host "Name: "$AIQ_ENTITY.name" / Count: "$AIQ_ENTITY.count" / ID: "$AIQ_ENTITY.id
} #>


### Step 4 - Get Information for each entity
foreach ($AIQ_ENTITY in $REST_SEARCH_RESPONSE.results ) {

    $API = $ENDPOINT+"/v2/"+$SEARCH_TYPE+"/"+$SEARCH_DEPTH+"/level/"+$SEARCH_CATEGORY+"/id/"+$AIQ_ENTITY.id
    $REST_RESPONSE = Invoke-RestMethod -Uri $API -Headers $HEADERS -Method GET
    
    Write-host ""
    Write-host $AIQ_ENTITY.name
    switch ($SEARCH_TYPE) {
        "capacity"{
            switch ($SEARCH_DEPTH) {
                "summary" {
                    Write-host ($REST_RESPONSE.($SEARCH_TYPE).count | Out-String).Trim()
                }
                "details" {
                    Write-host ($REST_RESPONSE.($SEARCH_TYPE).($SEARCH_DEPTH).current_90 | Out-String).Trim()
                    Write-host ($REST_RESPONSE.($SEARCH_TYPE).($SEARCH_DEPTH).("1_month_90") | Out-String).Trim()
                    Write-host ($REST_RESPONSE.($SEARCH_TYPE).($SEARCH_DEPTH).("3_months_90") | Out-String).Trim()
                    Write-host ($REST_RESPONSE.($SEARCH_TYPE).($SEARCH_DEPTH).("6_months_90") | Out-String).Trim()
                    Write-host ($REST_RESPONSE.($SEARCH_TYPE).($SEARCH_DEPTH).beyond6_months_90 | Out-String).Trim()
                }
                Default {
                    Write-host "Invalid search depth provided. Valid values are 'summary' and 'details'."
                    exit
                }
            }
        }
        "system"{
             Write-host ($REST_RESPONSE.results | Format-List | Out-String).Trim()

        }
        Default {
            Write-host "Invalid search category provided. Valid values are 'customer' and 'group'."
            exit
        }
    }
    
}