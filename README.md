# pamelafox-site
A personal homepage.

## Local development

This website is designed to be run inside a Docker contain, though the Flask app can also be run normally.

Build a Docker image:

```console
docker build --tag pamelafox-site .
```

Run the container:

```console
docker run -d -p 5000:5000 pamelafox-site
```

Then open the website at localhost:5000.

## Deployment instructions

This repository can be deployed as a container app on Microsoft Azure.

After creating a resource group, it can be deployed from the bicep file:

```
az deployment group create \
    --resource-group pamelafox-site-group \
    --template-file azure_cdn.bicep \
    --parameters googleApiKey=<SECRET> \
    -c
```

The custom domain should be mapped manually after deployment.


export RESOURCE_GROUP='pamelafox-swa-rg'
export RESOURCE_GROUP_LOCATION='eastus2'
export SWA_REPO_TOKEN=''
export SWA_NAME='pamelafox-swa-app'
export SWA_REPO_URL='https://github.com/pamelafox/pamelafox-site'
export SWA_REPO_BRANCH='master'
az group create -g $RESOURCE_GROUP -l $RESOURCE_GROUP_LOCATION

az deployment group create --resource-group $RESOURCE_GROUP --template-file infra/main.bicep --parameters swaName=$SWA_NAME swaRepositoryToken=$SWA_REPO_TOKEN swaRepositoryUrl=$SWA_REPO_URL swaRepositoryBranch=$SWA_REPO_BRANCH -c 