/*
Testing cloud-init custom_data, alternative solution in main.tf
*/

# data "template_file" "script_lempstack" {
#   template = file("${path.module}/scripts/runscript.sh")
# }

# data "template_cloudinit_config" "config_lempstack" {
#   gzip          = false
#   base64_encode = true

#   part {
#     content_type = "text/x-shellscript"
#     content      = data.template_file.script_lempstack.rendered
#   }
# }
