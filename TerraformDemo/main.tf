/*
Terraform automation deployment according to Lab1 and Lab2 in sequence
*/
# 1. Create resource group
resource "azurerm_resource_group" "rg-automate-test" {
  name     = "${var.naming}-resource-group"
  location = var.location
  tags = {
    unit    = "2206"
    project = "cloud-automation"
  }
}

# 2. Create Virtual Network and Subnet
# Create Virtual Network
resource "azurerm_virtual_network" "vn-automate-test" {
  name                = "${var.naming}-virtual-network"
  location            = azurerm_resource_group.rg-automate-test.location
  resource_group_name = azurerm_resource_group.rg-automate-test.name
  address_space       = ["10.2.0.0/16"]

  tags = {
    unit    = "2206"
    project = "cloud-automation"
  }
}

# Create Subnet
resource "azurerm_subnet" "sn-automate-test" {
  name                 = "${var.naming}-subnet"
  resource_group_name  = azurerm_resource_group.rg-automate-test.name
  virtual_network_name = azurerm_virtual_network.vn-automate-test.name
  address_prefixes     = ["10.2.0.0/24"]
}

# 3. Create Security Group
resource "azurerm_network_security_group" "sg-automate-test" {
  name                = "${var.naming}-security-group"
  location            = azurerm_resource_group.rg-automate-test.location
  resource_group_name = azurerm_resource_group.rg-automate-test.name

  # Security Rule to allow SSH
  #TODO: Remove default SSH port 22 and add port 1002 for SSH
  security_rule {
    name                       = "sshd"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Security Rule to allow http
  security_rule {
    name                       = "AllowhHttp"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Security Rule to allow https
  security_rule {
    name                       = "AllowHttps"
    priority                   = 120
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    unit    = "2206"
    project = "cloud-automation"
  }
}

# Associate Security Group to a Subnet
resource "azurerm_subnet_network_security_group_association" "sg-association" {
  subnet_id                 = azurerm_subnet.sn-automate-test.id
  network_security_group_id = azurerm_network_security_group.sg-automate-test.id
}

# 4. Create Public IP Address to communicate with the internet
resource "azurerm_public_ip" "pip-automate-test" {
  name                    = "${var.naming}-publicip"
  location                = azurerm_resource_group.rg-automate-test.location
  resource_group_name     = azurerm_resource_group.rg-automate-test.name
  ip_version              = "IPv4"
  sku                     = "Basic"
  allocation_method       = "Dynamic"
  idle_timeout_in_minutes = "4"
  domain_name_label       = "pip-automate-test"

  tags = {
    unit    = "2206"
    project = "cloud-automation"
  }
}

# 4. Create Cloud Instances
# Create Network Interface
resource "azurerm_network_interface" "nic-automate-test" {
  name                = "${var.naming}-nic"
  location            = azurerm_resource_group.rg-automate-test.location
  resource_group_name = azurerm_resource_group.rg-automate-test.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.sn-automate-test.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.pip-automate-test.id
  }
}

# Create Virtual Machine
resource "azurerm_linux_virtual_machine" "vmachine-automate-test" {
  name                = "${var.naming}-vmachine"
  resource_group_name = azurerm_resource_group.rg-automate-test.name
  location            = azurerm_resource_group.rg-automate-test.location

  size                  = "Standard_B1s"
  admin_username        = "adminuser"
  network_interface_ids = [azurerm_network_interface.nic-automate-test.id]

  # Cloud-init file, this script will be called with Virtual Machine has been deployed successfully
  //custom_data = filebase64("${path.module}/scripts/lempstack.tpl")
   custom_data = filebase64("${path.module}/scripts/lempstack.tpl")

  # Public key for SSH
  /*
  Options to pre-create ssh key or generate a new ssh key with terraform key gen
  1. ssh-keygen -t rsa (precreate)
  2. generate key pair every deployment and destroy every destruction (generate every deployment)
  */
  admin_ssh_key {
    username = "adminuser"
    # Ensure path to public key is correct
    # TODO: SCRIPTING TO LOOK FOR PUBKEY
    #public_key = file("~/.ssh/id_rsa.pub") # Linux environment
    public_key = file("${path.module}/keys/id_rsa.pub") # Current Windows environment
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    #offer     = "UbuntuServer"
    #sku       = "20.04-LTS"
    offer   = "0001-com-ubuntu-server-focal"
    sku     = "20_04-lts-gen2"
    version = "latest"
  }
}