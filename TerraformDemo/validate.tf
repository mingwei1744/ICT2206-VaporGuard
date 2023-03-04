resource "null_resource" "validate_config" {
  provisioner "local-exec" {
    command = "python validate_config.py ${var.tf_config_file}"
  }

  depends_on = [terraform.workspace]
}