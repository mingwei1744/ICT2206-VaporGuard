/*
Cloud-init custom_data
*/

# Template file for the respective scripts
data "template_file" "script_server_config" {
  template = file("${path.module}/scripts/config_server.tpl")

  vars = {
    rootUser = "${var.admin-user}"
    webUser  = "${var.web-user}"
  }
}

data "template_file" "script_lemp_config" {
  template = file("${path.module}/scripts/config_lemp.tpl")

  vars = {
    rootUser    = "${var.admin-user}"
    webUser     = "${var.web-user}"
    databasePwd = "${var.database-pwd}"
    domainName  = "${var.website-dns}"
  }
}

data "template_file" "script_web_config" {
  template = file("${path.module}/scripts/config_web.tpl")

  vars = {
    rootUser     = "${var.admin-user}"
    domainName   = "${var.website-dns}"
    emailAddress = "${var.email}"
  }
}

data "template_file" "script_php_xfer" {
  template = file("${path.module}/scripts/config_php_xfer.tpl")

}

# Consolidate into cloudinit config in sequence
data "template_cloudinit_config" "configs" {
  gzip          = false
  base64_encode = true

  # Run Part 1 (User, UFW)
  part {
    content_type = "text/x-shellscript"
    content      = data.template_file.script_server_config.rendered
  }
  # then Part 2 (LEMP stack)
  part {
    content_type = "text/x-shellscript"
    content      = data.template_file.script_lemp_config.rendered
  }

  # then Part 3 (HTTPS, HTTP2)
  part {
    content_type = "text/x-shellscript"
    content      = data.template_file.script_web_config.rendered
  }

  # then Part 4 (Transferring PHP files to html document root)
  part {
    content_type = "text/x-shellscript"
    content      = data.template_file.script_php_xfer.rendered
  }
}
