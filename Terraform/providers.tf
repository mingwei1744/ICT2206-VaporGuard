# Specify the version of the AzureRM Provider to use
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
}

# Configure the AzureRM Provider
# az login to retrieve cloud details
provider "azurerm" {
  features {}
}

