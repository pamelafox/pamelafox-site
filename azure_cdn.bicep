
@description('Name to prefix all created resources')
param name string = 'pamelafox-site'

@description('Url of the origin')
param originUrl string = 'pamelafox-site-container-app.redwater-9982941d.eastus2.azurecontainerapps.io'

@description('CDN SKU names')
@allowed([
  'Standard_Akamai'
  'Standard_Microsoft'
  'Standard_Verizon'
  'Premium_Verizon'
])
param CDNSku string = 'Standard_Microsoft'

@description('Name of the container registry')
param containerRegistryName string = 'pamelascontainerstore'

@description('Container image')
param containerImage string = 'pamelascontainerstore.azurecr.io/pamelafox-site:latest'

@secure()
@description('Google Spreadsheets API Key')
param googleApiKey string

@description('Location for all resources.')
param location string = resourceGroup().location

resource profile 'Microsoft.Cdn/profiles@2022-05-01-preview' = {
  name: '${name}-cdn-profile'
  location: location
  sku: {
    name: CDNSku
  }
}

resource endpoint 'Microsoft.Cdn/profiles/endpoints@2022-05-01-preview' = {
  parent: profile
  name: '${name}-cdn-endpoint'
  location: location
  properties: {
    originHostHeader: originUrl
    isHttpAllowed: true
    isHttpsAllowed: true
    queryStringCachingBehavior: 'IgnoreQueryString'
    contentTypesToCompress: [
      'application/eot'
      'application/font'
      'application/font-sfnt'
      'application/javascript'
      'application/json'
      'application/opentype'
      'application/otf'
      'application/pkcs7-mime'
      'application/truetype'
      'application/ttf'
      'application/vnd.ms-fontobject'
      'application/xhtml+xml'
      'application/xml'
      'application/xml+rss'
      'application/x-font-opentype'
      'application/x-font-truetype'
      'application/x-font-ttf'
      'application/x-httpd-cgi'
      'application/x-javascript'
      'application/x-mpegurl'
      'application/x-opentype'
      'application/x-otf'
      'application/x-perl'
      'application/x-ttf'
      'font/eot'
      'font/ttf'
      'font/otf'
      'font/opentype'
      'image/svg+xml'
      'text/css'
      'text/csv'
      'text/html'
      'text/javascript'
      'text/js'
      'text/plain'
      'text/richtext'
      'text/tab-separated-values'
      'text/xml'
      'text/x-script'
      'text/x-component'
      'text/x-java-source'
    ]
    isCompressionEnabled: true
    origins: [
      {
        name: 'origin1'
        properties: {
          hostName: originUrl
          originHostHeader: originUrl
          priority: 1
          weight: 1000
          enabled: true
        }
      }
    ]
  }
}


resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: 'workspace-pamelafoxsitegroupf8uf'
  location: '${location}2'
  properties: {
    sku: {
      name: 'pergb2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    workspaceCapping: {
      dailyQuotaGb: -1
    }
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}



resource containerEnv 'Microsoft.App/managedEnvironments@2022-03-01' = {
  name: '${name}-container-env'
  location: '${location}2'
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
    zoneRedundant: false
  }
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-02-01-preview' = {
  name: containerRegistryName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    policies: {
      quarantinePolicy: {
        status: 'disabled'
      }
      trustPolicy: {
        type: 'Notary'
        status: 'disabled'
      }
      retentionPolicy: {
        days: 7
        status: 'disabled'
      }
      exportPolicy: {
        status: 'enabled'
      }
      azureADAuthenticationAsArmPolicy: {
        status: 'enabled'
      }
      softDeletePolicy: {
        retentionDays: 7
        status: 'disabled'
      }
    }
    encryption: {
      status: 'disabled'
    }
    dataEndpointEnabled: false
    publicNetworkAccess: 'Enabled'
    networkRuleBypassOptions: 'AzureServices'
    zoneRedundancy: 'Disabled'
    anonymousPullEnabled: false
  }
}

var containerAppName = '${name}-container-app'

resource containerApp 'Microsoft.App/containerapps@2022-03-01' = {
  name: containerAppName
  location: '${location}2'
  identity: {
    type: 'None'
  }
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      secrets: [
        {
          name: 'registry-password'
          value: containerRegistry.listCredentials().passwords[0].value
        }
        {
          name: 'google-api-key'
          value: googleApiKey
        }
      ]
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 5000
        transport: 'Auto'
        traffic: [
          {
            weight: 100
            latestRevision: true
          }
        ]
        allowInsecure: false
      }
      registries: [
        {
          server: '${containerRegistry.name}.azurecr.io'
          username: containerRegistry.name
          passwordSecretRef: 'registry-password'
        }
      ]
    }
    template: {
      containers: [
        {
          image: containerImage
          name: containerAppName
          env: [
            {
              name: 'GOOGLE_API_KEY'
              secretRef: 'google-api-key'
            }
          ]
          resources: {
            cpu: '0.5'
            memory: '1Gi'
          }
        }
      ]
      scale: {
        maxReplicas: 10
      }
    }
  }
}
