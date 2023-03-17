<div align="center">
<h1> ICT2206 Assignment 1 </h1>
ICT2206 Web Security Assignment-1. The development of a defensive web application.
</div>

<div align="center">
<h1> VapourGuard 🛡️ </h1>
<p> Cloud security is a crucial aspect in today's digital landscape. The increasing adoption of cloud infrastructure to host web applications has motivated us to develop this tool, VaporGuard. </p>
<p> This tool focuses on validating web pre-deployments on a content delivery platform. Both the cloud configurations and web framework configurations will be analysed in a pre-deployment environment. </p>
</div>

## Pre-requisites and Setup 🛠️

### Requirements
* Azure cloud account
* Terraform
* Python3
* Any PDF reader (Browser, Adobe Reader etc.)

### Setup
1. Download [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) and add binary to PATH <br />
> Check if Terraform has been successfully installed <br />
```
terraform --version
```
2. Install [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli) (Skip this step if Step 3 is working)
> *Windows machine should be pre-installed with Azure CLI

3. Login to your Azure Account
```
az login
```
![azlogin](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/azlogin.png)

4. Install python dependencies
```
pip install -r requirements.txt
```

## Using VaporGuard 🤖
a) Generate a keypair in the /Terraform/keys directory. Example:
```
cd /Terraform/keys
ssh-keygen -t ecdsa -b 521
```
![keypair](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/keypair.png)

b) Start VaporGuard
```
python vaporguard.py start
```
![start](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/start.png)

c) Submit the relevant prompts for the infrastructure to be deployed
![level1](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/level1.png)

d) Analysis will commence once Step c. has been validated
![level2](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/level2.png)

e) A detailed report will be generated prior to the commencement of deployment
![report](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/report.png)

## Teardown 🗑
a) To remove all objects deployed
```
python vaporguard.py destroy
```
![destroy](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/todo.png)

