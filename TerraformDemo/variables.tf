/*
Custom variables, can be translated to python script as user input
tf_config_file is to be validated
*/
variable "location" {
  description = "Azure deployment location"
  type        = string
  default     = "East US"
}

variable "naming" {
  description = "Naming convention of objects"
  type        = string
  default     = "automato"
}

variable "dnsname" {
  description = "DNS naming"
  type        = string
  default     = "rg-2206-lab-dev-eastus-2102596"
}

variable "tf_config_file" {
  type    = string
  default = "A:/Users/JJ/Documents/GitHub/ICT2206-VapourGuard/TerraformDemo/main.tf"
}
