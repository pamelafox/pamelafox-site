param location string = resourceGroup().location
param swaName string

@allowed([ 'Free', 'Standard' ])
param swaSku string = 'Free'

@secure()
param swaRepositoryToken string
param swaRepositoryUrl string
param swaRepositoryBranch string

module staticWebApp 'swa.bicep' = {
    name: '${deployment().name}--swa'
    params: {
        location: location
        sku: swaSku
        name: swaName
        repositoryToken: swaRepositoryToken
        repositoryUrl: swaRepositoryUrl
        repositoryBranch: swaRepositoryBranch
    }
}
