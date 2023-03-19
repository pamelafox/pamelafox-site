targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

param domainName string = ''

var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Organize resources in a resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: '${environmentName}-rg'
  location: location
  tags: tags
}

// The SWA
module web 'swa.bicep' = {
  scope: rg
  name: '${environmentName}${resourceToken}-swa-module'
  params: {
    name: '${environmentName}${resourceToken}-swa'
    location: location
    tags: union(tags, { 'azd-service-name': 'web' })
    domainName: domainName
  }
}


// App outputs
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
