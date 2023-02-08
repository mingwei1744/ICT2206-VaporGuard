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