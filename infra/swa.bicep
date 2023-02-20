param name string
@allowed([ 'centralus', 'eastus2', 'eastasia', 'westeurope', 'westus2' ])
param location string
@allowed([ 'Free', 'Standard' ])
param sku string = 'Standard'
@secure()
param repositoryToken string
param repositoryUrl string
param repositoryBranch string = 'main'

resource swa_resource 'Microsoft.Web/staticSites@2021-01-15' = {
  name: name
  location: location
  tags: null
  properties: {
      // https://learn.microsoft.com/en-us/azure/static-web-apps/publish-azure-resource-manager?tabs=azure-cli#create-a-github-personal-access-token
      repositoryToken: repositoryToken
      repositoryUrl: repositoryUrl
      branch: repositoryBranch
      buildProperties: {
          appLocation: './'
          appBuildCommand: 'python3 freeze.py'
          outputLocation: './src/build'
      }
  }
  sku:{
      name: sku
      size: sku
  }
}
