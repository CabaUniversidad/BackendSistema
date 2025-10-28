# main.tf

# 1. Usa data "template_file" para procesar el script cloud_init.sh
data "template_file" "cloud_init_script" {
 template = file("${path.module}/cloud_init.sh")
}

resource "oci_core_instance" "Ubuntu_vm" {
 # Asegúrate de que este nombre sea ÚNICO, si no, tendrás el error 400.
 display_name        = "Ubuntu-docker-vm-04" # Ejemplo de nombre único
  
 availability_domain = var.availability_domain
 shape        = "VM.Standard.E2.1.Micro"
 compartment_id   = var.compartment_ocid

 source_details {
  source_type = "Image"
  source_id  = var.ubuntu_2204_image_ocid
 }

 create_vnic_details {
  subnet_id    = var.subnet_id
  assign_public_ip = true
  display_name   = "Ubuntu-docker-vm-vnic-04"
  # ¡Este debe ser el nombre ÚNICO en la subred!
  hostname_label  = "ubuntu-docker-vm-04" 
 }

 metadata = {
  ssh_authorized_keys = var.ssh_public_key
  # Envía el script completo de Bash, ya codificado en base64
  user_data      = base64encode(data.template_file.cloud_init_script.rendered)
 }
}

output "public_ip" {
 value = oci_core_instance.Ubuntu_vm.public_ip
}