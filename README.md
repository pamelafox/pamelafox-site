# pamelafox-site
A personal homepage.

## Deployment instructions

This repository can be deployed as a container app on Microsoft Azure.

After creating a resource group, it can be deployed from the bicep file:

```
az deployment group create --resource-group pamelafox-site-group --template-file azure_cdn.bicep --parameters googleApiKey=<SECRET> -c
```

The custom domain should be mapped manually after deployment.

