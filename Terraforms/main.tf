# Bloque requerido para configurar los proveedores
terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
    template = {
      source  = "hashicorp/template"
      version = "~> 2.2"
    }
  }
}

# Configuración del proveedor OCI
provider "oci" {
  tenancy_ocid = var.tenancy_ocid
  user_ocid    = var.user_ocid
  fingerprint  = var.fingerprint
  region       = var.region

  # ¡CAMBIO CLAVE! Ahora es la RUTA al archivo de la clave (no el contenido).
  private_key = var.ocid_private_key_path 
}

# 1. Usa data "template_file" para procesar el script cloud_init.sh
data "template_file" "cloud_init_script" {
  template = file("${path.module}/cloud_init.sh")
}

# Recurso de la instancia de la máquina virtual (Compute Instance)
resource "oci_core_instance" "Ubuntu_vm" {
  display_name        = "Ubuntu-docker-vm-04" 
  
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
    hostname_label  = "ubuntu-docker-vm-04" 
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key_content
    user_data          = base64encode(data.template_file.cloud_init_script.rendered)
  }
}

# Salida de la IP pública (necesaria para el despliegue SSH posterior)
output "public_ip" {
  value = oci_core_instance.Ubuntu_vm.public_ip
}
