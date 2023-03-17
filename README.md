<div align="center">
<h1> ICT2206 Assignment 1 </h1>
ICT2206 Web Security Assignment-1. The development of a defensive web application.
</div>

<div align="center">
<h1> VapourGuard 🛡️ </h1>
  <p> Cloud security is a crucial aspect in today's digital landscape. The increasing adoption of cloud infrastructure to host web applications has motivated us to develop this tool, VaporGuard. </p>
  <p> This tool focuses on validating web pre-deployments on a content delivery platform. Both the cloud configurations and web framework configurations will be analysed in a pre-deployment environment. </p>
  <img src="https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/todo.png" style="width: 75%; height: auto;"/>
</div>
<br />

## Pre-requisites and Setup
Vaporguard is tested on Windows environment. For Linux environment, please download the relevant binary from the respective website (Terraform, AzureCLI).
  
### Requirements ⚙️
* Azure cloud account
* Terraform
* Python3
* Any PDF reader (Browser, Adobe Reader etc.)

### Setup 🛠️
<b> 1. Download [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) and add binary to PATH. </b> <br />
> Check if Terraform has been successfully installed <br />
```
terraform --version
```
<b> 2. Install [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli) (Skip this step if Step 3 is working) </b> <br />
> *Windows machine should be pre-installed with Azure CLI

<b> 3. Login to your Azure Account </b> <br />
```
az login
```
![azlogin](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/azlogin.png)

<b> 4. Install python dependencies </b> <br />
```
pip install -r requirements.txt
```
<div align="center">
<h1> Using VaporGuard </h1>
</div>

## Starting deployment 🤖
<b> a) Generate a keypair in the /Terraform/keys directory. </b> <br/>
Example:
```
cd /Terraform/keys
ssh-keygen -t ecdsa -b 521
```
![keypair](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/keypair.png)

<b> b) Start VaporGuard </b>
```
python vaporguard.py start
```
![start](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/start.png)

<b> c) Submit the relevant prompts for the infrastructure to be deployed. </b>
![level1](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/level1.png)

<b> d) Analysis will commence once Step C. has been validated. A detailed report will then be generated. </b>
![level2](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/level2.png)
![report](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/report.png)

<b> e) Commence deployment </b>
![deploy](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/todo.png)
Once deployment is successful, the public IP of your web application will be shown. You may verify your resources in the Azure Cloud Portal.
![publicip](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/todo.png)

<b> f) Bind the public IP of your web application to the domain name submitted in Step C. </b> <br/>
Example (Porkbun):
![porkbun](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/todo.png)

## Teardown 🗑
<b> a) To remove all objects deployed </b>
```
python vaporguard.py destroy
```
![destroy](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/todo.png)

