/*
Custom variables, can be translated to python script as user input
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

variable "vm-dns" {
  description = "DNS for VM public IP"
  type        = string
  default     = "dns-xm-test" // CHANGE THIS TO YOUR PREFERRED VM DNS *UNQ
}

variable "admin-user" {
  description = "Admin user of server (root)"
  type        = string
  default     = "adminuser"
}

variable "web-user" {
  description = "Web application user of server"
  type        = string
  default     = "webadm"
}

variable "website-dns" {
  description = "Domain name for website public IP"
  type        = string
  default     = "WWW.YOURPBDOMAIN.COM" // CHANGE THIS TO YOUR PORKBUN DOMAIN NAME *UNQ
}

variable "database-pwd" {
  description = "Access code for database"
  type        = string
  default     = "dbP@assw0rd"
}

variable "email" {
  description = "Email for certbot"
  type        = string
  default     = "YOUREMAIL@EMAIL.COM" // CHANGE TO YOUR EMAIL
}

variable "web-codes" {
  description = "Directory for web upload"
  type        = string
  default     = "./Terraform/php/"
}