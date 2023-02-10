# ICT2206 Assignment 1
ICT2206 Web Security Assignment-1. The development of a defensive web application.

## VapourGuard 🛡️
Validating Web deployments on content delivery platform.

## Setup
1. Download [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) and add binary to PATH <br />
> Check if Terraform has been successfully installed <br />
```
terraform --version
```
2. Install [Azure CLI](https://developer.hashicorp.com/terraform/downloads) (Skip this step if Step 3 is working)
> *Windows machine should be pre-installed with Azure CLI

3. Login to your Azure Account
```
az login
```
![azlogin](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/azlogin.png)

## Deployment
a) Generate a key in the /TerraformDemo/keys directory (Mimicking Lab steps)
> *Do not commit the keys to the Github repo! 
```
cd /TerraformDemo/keys
ssh-keygen -t ecdsa -b 521
```
![keypair](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/keypair.png)

b) Edit your domain name in /TerraformDemo/scripts/lempstack.tpl
> E.g., www.my-domain.com ; Remember to bind your domain name in Porkbun after deployment
![domainname](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/domain.png)

c) Initialize a working directory containing Terraform configuration files.
> From the main working directory /TerraformDemo run terraform init
```
terraform init
```

d) Preview execution plan
> From the main working directory /TerraformDemo run terraform plan.
```
terraform plan
```

e) Start deployment
> From the main working directory /TerraformDemo run terraform apply.
```
terraform apply
```

**Pending TODOs commented in the script
