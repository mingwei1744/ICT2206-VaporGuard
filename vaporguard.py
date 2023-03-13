import os
import sys
import re
import time
import requests
from termcolor import colored
from Configpackage.configclass import UserConfig
from Configpackage.phpvulnchecker import *

terraformDir = "Terraform"

def logo():
    print(colored(""" 
    ##``````##``:::####:::``#########:``:########:``#########:
    ##``````##``##::::::##``##:::::::#``##::::::##``##:::::::#
    ##``````##``##::::::##``##:::::::#``##::::::##``##:::::::#
    `##````##```##::::::##``########::``##::::::##``#########:
    `##````##```##########``##``````````##::::::##``####::````
    `##````##```##``````##``##``````````##::::::##``##``###:``
    ``##``##````##``````##``##``````````##::::::##``##```###:`
    ````##``````##``````##``##``````````:########:``##`````###
    ``````````````````````````````````````````````````````````
    ``````````````````````````````````````````````````````````
    :#########``##``````##``:::####:::``#########:``#########:
    ###`````````##``````##``##::::::##``##:::::::#``##::::::##
    ##``````````##``````##``##::::::##``##:::::::#``##::::::##
    ##``````````##``````##``##::::::##``#########:``##::::::##
    ##``#####:``##``````##``##########``####::``````##::::::##
    ##``````##``##``````##``##``````##``##``###:````##::::::##
    ##``````##``##``````##``##``````##``##```###:```##::::::##
    :#########``:########:``##``````##``##`````###``#########:
    """, "cyan", attrs=["blink", "bold"]))
    print(colored("*" * 90, "yellow"))

def bannerG():
    print(colored("Next >>>", "green"))
    print(colored("+" * 90, "green"))

def bannerR():
    print(colored("Reverting...", "red"))
    print(colored("x" * 90, "red"))

def warningPrint(msg):
    print(colored(msg, "red", attrs=["bold"]))

def inputPrint(msg):
    print(colored(msg, "yellow", attrs=["bold", "blink"]))

def check_empty_input(data):
    empty = ''
    isempty = True

    if data != empty:
        isempty = False
    else:
        isempty = True

    return isempty

conf = UserConfig()
# -------------------------------------------------------------------------------
# Start of VaporGuard program
# Get user input
# TODO: Add a stage to generate keypair? Currently manual generation of key by user.
# However, if no keypair is being generated, deployment will not be successful.
# -------------------------------------------------------------------------------
# Wrapper function, signifying the start of the program
def config_init():
    logo()
    config_resource_name()

# Function to check valid naming convention for Azure resources
def check_valid_naming(input_str):
    if not any(char.isalpha() for char in input_str):
        return False
    return all(char.isalnum() or char == '-' for char in input_str)

# Function to get resource name
def config_resource_name():
    resource_name = input(colored(
        "1. Enter naming convention for all objects to be deployed on Azure Cloud: ", "blue", attrs=['bold']))

    if check_empty_input(resource_name) == False:
        if check_valid_naming(resource_name):
            conf.set_resource_naming(resource_name)
            inputPrint("Resource naming: " + resource_name)
            bannerG()
            # Next
            config_vm_dns()
        else:
            warningPrint("Invalid resource naming")
            bannerR()
            config_resource_name()
    else:
        warningPrint("Resource name cannot be empty")
        bannerR()
        config_resource_name()

# Function to get VM DNS name
def config_vm_dns():
    vm_dns_name = input(colored(
        "2. Enter Virtual Machine DNS Name: ", "blue", attrs=['bold']))

    if check_empty_input(vm_dns_name) == False:
        if check_valid_naming(vm_dns_name):
            conf.set_vm_dns(vm_dns_name)
            inputPrint("VM DNS name: " + vm_dns_name)
            bannerG()
            # Next
            config_root_user()
        else:
            warningPrint("Invalid VM DNS naming")
            bannerR()
            config_vm_dns()
    else:
        warningPrint("VM DNS name cannot be empty")
        bannerR()
        config_vm_dns()

# Function to get VM root username 
# TODO: CHECK FOR UNUSABLE AZURE USERNAME
def config_root_user():
    vm_root_user = input(colored(
        "3. Enter root username for Virtual Machine: ", "blue", attrs=['bold']))

    if check_empty_input(vm_root_user) == False:
        if vm_root_user.isalnum():
            conf.set_rootuser(vm_root_user)
            inputPrint("VM Root Username: " + vm_root_user)
            bannerG()
            # Next
            config_web_user()
        else:
            warningPrint("Invalid username")
            bannerR()
            config_root_user()
    else:
        warningPrint("VM root user cannot be empty")
        bannerR()
        config_root_user()

# Function to get VM web username
# F: Change to YES/NO create seperate user for web administrator? If NO, flag to report
# TODO: CHECK IF WEBUSER != ROOTUSER
def config_web_user():
    vm_web_user = input(colored(
        "4. Enter web admin username for Virtual Machine: ", "blue", attrs=['bold']))

    if check_empty_input(vm_web_user) == False:
        if vm_web_user.isalnum():
            conf.set_webuser(vm_web_user)
            inputPrint("VM Web Admin Username: " + vm_web_user)
            bannerG()
            # Next
            config_domain_name()
        else:
            warningPrint("Invalid username")
            bannerR()
            config_web_user()
    else:
        warningPrint("VM web admin user cannot be empty")
        bannerR()
        config_web_user()

# Function to get website domain name
def check_valid_domain(domain):
    pattern = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    if re.match(pattern, domain):
        return True
    else:
        return False

def config_domain_name():
    web_domain = input(colored(
        "5. Enter domain name for website: ", "blue", attrs=['bold']))

    if check_empty_input(web_domain) == False:
        if check_valid_domain(web_domain):
            conf.set_web_domain_name(web_domain)
            inputPrint("Website domain name: " + web_domain)
            bannerG()
            # Next
            config_database_key()
        else:
            warningPrint("Invalid domain name")
            bannerR()
            config_domain_name()
    else:
        warningPrint("No domain name entered")
        bannerR()
        config_domain_name()

# Function to get database password
def check_valid_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$"
    if re.match(pattern, password):
        return True
    else:
        return False

def config_database_key():
    print(colored("Access key should meet the following criteria:\n \
        - It is alphanumeric. \n \
        - It contains at least 12 characters.\n \
        - It contains at least one special character. \n \
        - It contains at least one uppercase and lowercase letter.", "blue", attrs=['bold']))
    database_key = input(colored(
        "6. Enter database key: ", "blue", attrs=['bold']))
    
    if check_empty_input(database_key) == False:
        if check_valid_password(database_key):
            conf.set_database_key(database_key)
            inputPrint("Database access key: " + database_key)
            bannerG()
            # Next
            config_email_address()
        else:
            warningPrint("Database access key did not meet the criteria")
            bannerR()
            config_database_key()
    else:
        warningPrint("Database access key cannot be empty")
        bannerR()
        config_database_key()

# Function to get email address for SSL cert
def check_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email):
        return True
    else:
        return False

def config_email_address():
    email_address = input(colored(
        "7. Enter your email address for SSL cert: ", "blue", attrs=['bold']))
    
    if check_empty_input(email_address) == False:
        if check_valid_email(email_address):
            conf.set_email(email_address)
            inputPrint("Email address: " + email_address)
            bannerG()
            # Next
            config_web_codes()
        else:
            warningPrint("Invalid email address")
            bannerR()
            config_email_address()
    else:
        warningPrint("An email address is required for SSL cert")
        bannerR()
        config_email_address()

# Function to get php directory
def find_php_directory(path):
    directories = []
    for root, dirs, files in os.walk(path):
        if any(file.endswith(('.php', '.html', '.js')) for file in files):
            dir = root.replace("\\", "/")
            directories.append(dir + "/")
    return directories

def config_web_codes():
    dirs = find_php_directory("./")
    for dir in range(len(dirs)):
        print(colored(f"{dir+1}) {dirs[dir]}", "blue", attrs=['bold']))
    
    if len(dirs) !=0:
        web_codes_dir = input(colored(f"8. Select directory of web codes to upload [1-{len(dirs)}]: ", "blue", attrs=['bold']))

        if check_empty_input(web_codes_dir) == False:
            conf.set_web_codes(dirs[int(web_codes_dir)-1])
            inputPrint("Web code directory: " + dirs[int(web_codes_dir)-1])
            bannerG()
            # Next
            create_tfvars()
        else:
            warningPrint("Please select which directory to upload")
            bannerR()
            config_web_codes()

    else:
        warningPrint("No web codes found in current workspace. Please add your web files to upload")
        bannerR()
        config_web_codes()

# -------------------------------------------------------------------------------
# Create tfvars file with user input
# -------------------------------------------------------------------------------
def val_wrap(val):
    # str values
    if type(val) == str:
        val = "\"" + val + "\""

    else:
        warningPrint(f"Error in tfvars value representation: {val}")

    return val

# Writing user input to tfvars
def create_tfvars():
    tfvar_cf = os.getcwd() + f"\\{terraformDir}\\userconfig.auto.tfvars"
    tfvar_config_file = tfvar_cf.replace("\\", "/")
    
    file = open(tfvar_config_file, "w")

    config_resource_naming = "naming = " + val_wrap(conf.get_resource_naming())
    config_vm_dns = "vm-dns = " + val_wrap(conf.get_vm_dns())
    config_root_user = "admin-user = " + val_wrap(conf.get_rootuser())
    config_webadm_user = "web-user = " + val_wrap(conf.get_webuser())
    config_web_domain = "website-dns = " + val_wrap(conf.get_web_domain_name())
    config_database_key = "database-pwd = " + val_wrap(conf.get_database_key())
    config_email_address = "email = " + val_wrap(conf.get_email())
    config_web_codes = "web-codes = " + val_wrap(conf.get_web_codes())

    configs = [config_resource_naming, config_vm_dns, config_root_user, config_webadm_user, config_web_domain, config_database_key, config_email_address, config_web_codes]

    for config in configs:
        file.write(config)
        file.write("\n")

    file.close()

    # Next, Generate detailed report on full stack
    print(colored("Generating Detailed Report...", "green", attrs=["bold"]))
    generate_detailed_report()
        
# -------------------------------------------------------------------------------
# Generate Report
# -------------------------------------------------------------------------------
def generate_detailed_report():
    
    # TODO: Generate Cloud Config Report

    # TODO: Generate Config Scripts Report

    # Generate PHP Report
    # Get all vulnerabilities IDs
    vuln_ids_arr = []
    get_rule_values("id", vuln_ids_arr)

    # Get all php files
    php_files_dir = "./vulns/" # Specify directory with php file TODO: Get vuln php codes
    #php_files_dir = conf.get_web_codes()
    php_files_arr = []
    get_php_files(php_files_dir, php_files_arr)

    # Store results into a dictionary
    vuln_results_consolidated = {}
    for phpfiles in php_files_arr:
        phpfile = php_files_dir + phpfiles
        for vuln_id in vuln_ids_arr:
            # Generate results with phpfile, checker(), store_in_dict
            store_results(phpfile, php_vuln_checker2(phpfile, vuln_id), vuln_results_consolidated)

    generate_php_report(vuln_results_consolidated, php_files_dir)

    # Merge?
    # Open report and ask for user prompt to continue


    # Prompt user to proceed
    begin_deployment()

# -------------------------------------------------------------------------------
# Terraform Deployment
# -------------------------------------------------------------------------------
def begin_deployment():

    deploy_confirmation = input(
        colored("Ready to start? (Y/N): ", "blue", attrs=["bold"]))

    # Agrees to begin deployment
    if deploy_confirmation.upper() == "Y" or deploy_confirmation.upper() == "YES":
        # Render .auto.tfvars tfile after user confirmation
        # next
        bannerG()
        #tf_init()

    # Do not agree to being deployment
    elif deploy_confirmation.upper() == "N" or deploy_confirmation.upper() == "N":

        exit_config = input(colored(
            "> Are you sure you want to exit configuration? (Y/N): ", "blue", attrs=["bold"]))

        if exit_config.upper() == "Y" or exit_config.upper() == "YES":
            print(colored("Exiting program...", "yellow", attrs=["bold"]))
            sys.exit()

        elif exit_config.upper() == "N" or exit_config.upper() == "NO":
            begin_deployment()

        else:
            warningPrint("Invalid input. \n")
            bannerR()
            begin_deployment()

    else:
        warningPrint("Invalid input. \n")
        bannerR()
        begin_deployment()

# Function to start Terraform deployment
def tf_init():
    # Checker for successful Terraform deployment
    success = 0

    sud = os.getcwd() + f"\\{terraformDir}"
    dir = sud.replace("\\", "/")
    os.chdir(dir)

    # Terraform init
    tf_init = terraform_init()

    if tf_init == success:
        # Terraform plan
        tf_plan = terraform_plan()

        if tf_plan == success:
            # Terraform apply
            tf_apply = terraform_apply()

            if tf_apply == success:
                print(colored("Please proceed to your domain name provider for domain name binding", "green", attrs=["bold"]))
                print(colored("Checking for deployment status...", "grey", attrs=["bold"]))
                os.chdir("../")
                time.sleep(10)

                check_count = 0
                while check_web_status() == False:
                    check_count += 1
                    print(colored(f"Waiting for deployment to complete... [{check_count}]", "grey", attrs=["bold"]))
                    time.sleep(60)
                    check_web_status()

                    if check_count == 15:
                        warningPrint("Exceeded configuration time. Please check on Terraform output")
                        sys.exit()

                    if check_web_status():
                        print(colored("Terraform deployment executed successfully", "green", attrs=["bold"]))
                        sys.exit()
            else:
                warningPrint("An error occurred at Terraform deployment stage.")
                sys.exit()
        else:
            warningPrint("An error occurred at Terraform plan stage.")
            sys.exit()
    else:
        warningPrint("An error occurred at Terraform init stage.")
        sys.exit()

# Function to init Terraform deployment
def terraform_init():
    os.system("terraform fmt")
    tf_init = "terraform init"
    val = os.system(tf_init)

    return val

# Terraform plan - preview execution plan for checking and error alerts (or change to validate to reduce console output)
def terraform_plan():
    tf_plan = "terraform plan"
    val = os.system(tf_plan)

    return val

# Terraform apply - executes the actions proposed in a Terraform plan
def terraform_apply():
    tf_apply = "terraform apply -auto-approve"
    val = os.system(tf_apply)

    return val

# Function to get website status
def check_web_status():
    try:
        response = requests.get(conf.get_web_domain_name())
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


# Main 
if __name__ == "__main__":
    try:
        config_init()

    except KeyboardInterrupt:
        warningPrint("\nExiting configuration...")
        #os.chdir(os.getcwd() + f"/{terraformDir}")
        #os.remove("userconfig.auto.tfvars")
        sys.exit()