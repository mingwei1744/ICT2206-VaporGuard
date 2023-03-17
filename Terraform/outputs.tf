/*
This file contains all the output to be presented to the user
*/
data "azurerm_public_ip" "vm-ip-data" {
  name                = azurerm_public_ip.pip-vpguard.name
  resource_group_name = azurerm_resource_group.rg-vpguard.name
  depends_on = [
    azurerm_public_ip.pip-vpguard,
    azurerm_linux_virtual_machine.vmachine-vpguard
  ]
}

output "website_public_ip" {
  value       = data.azurerm_public_ip.vm-ip-data.ip_address
  description = "Public IP of Azure VM"
}