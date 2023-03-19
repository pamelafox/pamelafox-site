param name string
param location string = resourceGroup().location
param tags object = {}

param domainName string = ''

param sku object = {
  name: 'Free'
  tier: 'Free'
}

resource web 'Microsoft.Web/staticSites@2022-03-01' = {
  name: name
  location: location
  tags: tags
  sku: sku
  properties: {
    provider: 'Custom'
  }
}

// Necessary due to https://github.com/Azure/bicep/issues/9594
// placeholderName is never deployed, it is merely used to make the child name validation pass
var domainNameForBicep = !empty(domainName) ? domainName : 'placeholderName'

resource swaDomain 'Microsoft.Web/staticSites/customDomains@2022-03-01' = if (!empty(domainName)) {
  name: domainNameForBicep
  kind: 'string'
  parent: web
  properties: {
    validationMethod: 'cname-delegation'
  }
}

output name string = web.name
output uri string = 'https://${web.properties.defaultHostname}'
