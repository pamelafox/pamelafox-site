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

