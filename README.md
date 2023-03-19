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
flask --debug run
```

Then open the website at localhost:5000.

## Deployment instructions

This project is designed for deployment on Azure Static Web Apps.

Steps for deployment:

1. Sign up for a [free Azure account](https://azure.microsoft.com/free/)
2. Install the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd). (If you opened this repository in a Dev Container, that part will be done for you.)
3. Provision and deploy all the resources:

    ```shell
    azd up
    ```

    It will prompt you to login and to provide a name (like "mysite") and location. Then it will provision the resources in your account and deploy the latest code.

4. When `azd` has finished deploying, you'll see an endpoint URI in the command output. Visit that URI to see the website.

5. When you've made any changes to the app code, you can just run:

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
