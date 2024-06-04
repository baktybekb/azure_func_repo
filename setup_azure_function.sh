##!/bin/bash
#
## Variables (update these with your own values)
#RESOURCE_GROUP_NAME="bahaResourceGroup"
#LOCATION="eastus"
#STORAGE_ACCOUNT_NAME="bahastorageaccount"  # Storage account names must be unique
#FUNCTION_APP_NAME="bahaFunctionApp"  # Function app names must be unique
#PLAN_NAME="bahaLinuxPlan"
#AZURE_SUBSCRIPTION_ID="2d789d7d-5f4a-4fb2-9f1e-bab95f36b81a"
#SERVICE_CONNECTION_NAME="bahaServiceConnection"
#ORGANIZATION_URL="https://dev.azure.com/bahaProject"
#PROJECT_NAME="azureFuncProject"
#
## Ensure jq is installed
#if ! command -v jq &> /dev/null
#then
#    echo "jq could not be found. Installing jq..."
#    sudo apt-get update
#    sudo apt-get install -y jq
#fi
#
## Create Resource Group
#echo "Creating resource group..."
#az group create --name $RESOURCE_GROUP_NAME --location $LOCATION
#
## Create Storage Account
#echo "Creating storage account..."
#az storage account create --name $STORAGE_ACCOUNT_NAME --location $LOCATION --resource-group $RESOURCE_GROUP_NAME --sku Standard_LRS
#
## Create an App Service Plan for Linux
#echo "Creating App Service plan..."
#az appservice plan create --name $PLAN_NAME --resource-group $RESOURCE_GROUP_NAME --location $LOCATION --is-linux --sku B1
#
## Create Function App in Linux environment
#echo "Creating function app in Linux environment..."
#az functionapp create --resource-group $RESOURCE_GROUP_NAME --plan $PLAN_NAME --runtime python --runtime-version 3.10 --functions-version 4 --name $FUNCTION_APP_NAME --storage-account $STORAGE_ACCOUNT_NAME
#
## Generate Deployment Credentials
#echo "Generating deployment credentials..."
#DEPLOYMENT_CREDENTIALS=$(az functionapp deployment list-publishing-profiles --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP_NAME)
#FTP_USERNAME=$(echo $DEPLOYMENT_CREDENTIALS | jq -r '.[0].userName')
#FTP_PASSWORD=$(echo $DEPLOYMENT_CREDENTIALS | jq -r '.[0].userPWD')
#
## Install Azure DevOps extension
#echo "Installing Azure DevOps extension..."
#az extension add --name azure-devops
#
## Configure default organization and project
#echo "Configuring Azure DevOps defaults..."
#az devops configure --defaults organization=$ORGANIZATION_URL project=$PROJECT_NAME
#
## Create service principal and get appId, password, and tenant
#echo "Creating service principal..."
#SP_JSON=$(az ad sp create-for-rbac --name http://$SERVICE_CONNECTION_NAME --role contributor --scopes /subscriptions/$AZURE_SUBSCRIPTION_ID)
#APP_ID=$(echo $SP_JSON | jq -r '.appId')
#PASSWORD=$(echo $SP_JSON | jq -r '.password')
#TENANT=$(echo $SP_JSON | jq -r '.tenant')
#
## Export the service principal key as an environment variable
#export AZURE_DEVOPS_EXT_AZURE_RM_SERVICE_PRINCIPAL_KEY=$PASSWORD
#
## Verify the environment variable is set
#echo "Azure RM service principal key: $AZURE_DEVOPS_EXT_AZURE_RM_SERVICE_PRINCIPAL_KEY"
#
## Create service connection
#echo "Creating service connection..."
#az devops service-endpoint azurerm create --name $SERVICE_CONNECTION_NAME --azure-rm-service-principal-id $APP_ID --azure-rm-subscription-id $AZURE_SUBSCRIPTION_ID --azure-rm-subscription-name "My Subscription" --azure-rm-tenant-id $TENANT --org $ORGANIZATION_URL --project $PROJECT_NAME
#
#echo "Setup complete. Your Azure Function App '$FUNCTION_APP_NAME' is ready, and the service connection '$SERVICE_CONNECTION_NAME' has been created in Azure DevOps."
