/*
This file contains all the output to be presented to the user
*/
data "azurerm_public_ip" "vm-ip-data" {
  name                = azurerm_public_ip.pip-automate-test.name
  resource_group_name = azurerm_resource_group.rg-automate-test.name
  depends_on = [
    azurerm_public_ip.pip-automate-test,
    azurerm_linux_virtual_machine.vmachine-automate-test
  ]
}

output "website_public_ip" {
  value       = data.azurerm_public_ip.vm-ip-data.ip_address
  description = "Public IP of Azure VM"
}