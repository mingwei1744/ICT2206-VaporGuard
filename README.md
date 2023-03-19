<div align="center">
<h1> ICT2206 Assignment 1 </h1>
ICT2206 Web Security Assignment-1. The development of a defensive web application.
</div>

<div align="center">
<h1> VaporGuard 🛡️ </h1>
  <p> Cloud security is a crucial aspect in today's digital landscape. The increasing adoption of cloud infrastructure to host web applications has motivated us to develop this tool, VaporGuard. </p>
  <p> This tool focuses on validating web pre-deployments on a content delivery platform. Both the cloud configurations and web framework configurations will be analysed in a pre-deployment environment. </p>
  <img src="https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/logo.png" style="width: auto; height: auto;"/>
</div>
<br />

## Pre-requisites and Setup
Vaporguard is tested on Windows environment. For Linux environment, please download the relevant binary from the respective website (Terraform, AzureCLI).
  
### Requirements ⚙️
* Azure cloud account
* Terraform
* Python3
* OpenAI API key
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
<b> 4. Request for OpenAI API key </b> <br />
* Generate an OpenAI API key here, https://platform.openai.com/account/api-keys
![OpenAIAPIKey](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/openai_request_API_key.jpg)
* Replace the openai.api_key in the Configpackage/validate_cloud.py
```
    # Make the API request with your own API KEY
    openai.api_key = "sk-12345"
```
<b> 5. Install python dependencies </b> <br />
```
pip install -r requirements.txt
```
<div align="center">
<h1> Using VaporGuard </h1>
</div>

## Starting deployment 🤖
<b> a) Define your keypairs, cloud-init scripts and PHP files. </b> <br/>
* Generate a keypair in the /Terraform/keys directory:
```
cd /Terraform/keys
ssh-keygen -t ecdsa -b 521
```
![keypair](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/keypair.png)
<br />

* Upload your PHP codes in the /Terraform/html directory. <br/>
```
cd /Terraform/html
```
![php](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/php.png)
<br />

<b> b) Start VaporGuard </b> <br/>
```
python vaporguard.py start
```
![start](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/start.png)
<br />

<b> c) Submit the relevant prompts for the infrastructure to be deployed. </b> <br/>
![level1](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/level1.png)
<br />

<b> d) Analysis will commence once Step C. has been validated. A detailed report will then be generated. </b> <br/>
![level2](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/level2.png)
<br />
![report](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/report.png)
<br />

<b><ins> Report Structure </ins></u>
|Result Sections |Parameters      |
|----------------|----------------|
|Cloud Configs|<ul><li>check ID</li><li>File</li><li>Line</li><li>Potential CVE/CWE</li><li>Guildline URL</li><li>Status</li</ul>|
|Scripts Configs|<ul><li>File name</li><li>Line</li><li>Severity</li><li>Verified</li><li>Details</li></ul>|
|PHP Configs|<ul><li>File name</li><li>Line</li><li>Vulnerability ID</li><li>Details</li><li>Serverity</li><li>OWAPS #</li><li>CWE #</li><li>Recommendations</li></ul>|

<b> e) Commence deployment </b> <br/>
After reviewing through the vulnerability report, to continue deployment, close the report and proceed. <br/>
![deploy](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/deploy.png)
<br/>
Once deployment is successful, the public IP of your web application will be shown. You may verify your resources in the Azure Cloud Portal. <br/>
![publicip](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/publicip.png)
<br />

<b> f) Bind the public IP of your web application to the domain name submitted in Step C. </b> <br/>

## Teardown 🗑
<b> a) To remove all objects deployed </b> <br/>
```
python vaporguard.py destroy
```
![teardown](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/teardown.png)
<br />
![destroy](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/destroy.png)

 ## Youtube Demo 📹
[![Watch the video](https://github.com/mingwei1744/ICT2206-VapourGuard/blob/main/Images/thumbnail.png)](https://youtu.be/H0T3Ft_bDA4)
