# pamelafox-site
A personal homepage.

## Local development


```shell
pip install -r requirements-dev.txt
```

```shell
pre-commit install
```

```shell
flask run
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
