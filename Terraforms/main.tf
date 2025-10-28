# Archivo: Terraforms/main.tf

# Bloque requerido para configurar los proveedores
terraform {
  required_providers {
    # Utilizamos el proveedor oficial 'oracle/oci' como recomienda Terraform
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
    # Mantener el proveedor 'template' para cloud-init
    template = {
      source  = "hashicorp/template"
      version = "~> 2.2"
    }
  }
}

# Configuración del proveedor OCI
provider "oci" {
  # Las siguientes variables se pasan como TF_VAR_<nombre> desde GitHub Actions
  tenancy_ocid = var.tenancy_ocid
  user_ocid    = var.user_ocid
  fingerprint  = var.fingerprint
  region       = var.region

  # CORREGIDO: Usamos el contenido de la clave, que ahora está declarado en variables.tf
  private_key = var.private_key_content
}

# 1. Usa data "template_file" para procesar el script cloud_init.sh
data "template_file" "cloud_init_script" {
 template = file("${path.module}/cloud_init.sh")
}

# Recurso de la instancia de la máquina virtual (Compute Instance)
resource "oci_core_instance" "Ubuntu_vm" {
 # Asegúrate de que este nombre sea ÚNICO, si no, tendrás el error 400.
 display_name        = "Ubuntu-docker-vm-04" # Ejemplo de nombre único
  
 availability_domain = var.availability_domain
 shape               = "VM.Standard.E2.1.Micro"
 compartment_id      = var.compartment_ocid

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
  # CORREGIDO: Usamos la variable de contenido, que ahora está declarado en variables.tf
  ssh_authorized_keys = var.ssh_public_key_content
  # Envía el script completo de Bash, ya codificado en base64
  user_data      = base64encode(data.template_file.cloud_init_script.rendered)
 }
}

# Salida de la IP pública (necesaria para el despliegue SSH posterior)
output "public_ip" {
 value = oci_core_instance.Ubuntu_vm.public_ip
}