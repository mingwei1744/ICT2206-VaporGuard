import os
import sys
from termcolor import colored

# Terraform destroy
def terraform_destroy():
    sud = os.getcwd() + "\\Terraform"
    dir = sud.replace("\\", "/")
    os.chdir(dir)

    tf_destroy = "terraform destroy -auto-approve"
    val = os.system(tf_destroy)

    return val

def cleanup_vars():
    sud = os.getcwd() + "\\Terraform"
    dir = sud.replace("\\", "/")
    os.chdir(dir)

    if os.path.exists("userconfig.auto.tfvars"):
        os.remove("userconfig.auto.tfvars")


def destroy():
    success = 0

    print(colored("Warning!, all data configured will be deleted", "red", attrs=['bold']))
    destroy = input(colored("Are you sure you want to destroy the deployed infrastructures? (Y/N): ", "blue", attrs=['bold']))

    if destroy.upper() == "Y" or destroy.upper() == "YES":
        tf_destroy = terraform_destroy()

        if tf_destroy == success:
            print(colored("Terraform infrastructure destroyed and cleaned up", "green", attrs=['bold']))
            sys.exit()

        else:
            print(colored("An error occurred when destroying infrastructures. Please see stderr above for more info", "red", attrs=['bold']))
            sys.exit()

    elif destroy.upper() == "N" or destroy.upper() == "NO":
        sys.exit()

    else:
        print(colored("Invalid input. \n", "red"))
        destroy()