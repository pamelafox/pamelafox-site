# pamelafox-site
A personal homepage.

## Local development


```shell
python3 -m pip install -r requirements-dev.txt
```

```shell
pre-commit install
```

```shell
flask --debug --app src/app:app run --port 50505
```

Then open the website at localhost:5000.

## Deployment instructions

This project is designed for deployment on Azure Static Web Apps.

Steps for deployment:

1. Sign up for a [free Azure account](https://azure.microsoft.com/free/)
2. Install the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd). (If you opened this repository in a Dev Container, that part will be done for you.)
3. Initialize a new `azd` environment:

    ```shell
    azd init
    ```

    It will prompt you to provide a name (like "mysite") that will later be used in the name of the deployed resources.

4. Provision and deploy all the resources:

    ```shell
    azd up
    ```

    It will prompt you to login, pick a subscription, and provide a location (like "eastus"). Then it will provision the resources in your account and deploy the latest code.

5. When `azd` has finished deploying, you'll see an endpoint URI in the command output. Visit that URI to see the website.

6. When you've made any changes to the app code, you can just run:

    ```shell
    azd deploy
    ```

## CI/CD pipeline

This project includes a Github workflow for deploying the resources to Azure
on every push to main. That workflow requires several Azure-related authentication secrets
to be stored as Github action secrets. To set that up, run:

```shell
azd pipeline config
```
