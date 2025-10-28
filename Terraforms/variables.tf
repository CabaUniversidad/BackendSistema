variable "tenancy_ocid" {
    description = "El OCID del arrendamiento (tenancy)" 
    type        = string
}
# ... (user_ocid, fingerprint, region, compartment_ocid, subnet_id, availability_domain, ubuntu_2204_image_ocid siguen igual)

variable "private_key_path" {
    # ¡CORRECCIÓN CLAVE! Revertido a private_key_path
    description = "La ruta al archivo de la clave privada API (oci_api_key.pem)" 
    type        = string
}

variable "ssh_public_key_content" {
    description = "El contenido RAW de la clave pública SSH para acceder a la instancia" 
    type        = string
}

variable "user_ocid" {
    description = "El OCID del usuario" 
    type        = string
}

variable "fingerprint" {
    description = "La huella digital de la clave pública del usuario" 
    type        = string
}

variable "private_key_content" {
    # ¡CORREGIDO! Cambiado de private_key_path a private_key_content
    description = "El contenido RAW de la clave privada API (Secret: SSH_PRIVATE_KEY)" 
    type        = string
}

variable "region" {
    description = "La región de Oracle Cloud" 
    type        = string
}

variable "compartment_ocid" {
    description = "El OCID del compartimiento" 
    type        = string
}

variable "subnet_id" {
    description = "El OCID de la subred" 
    type        = string
}

variable "availability_domain" {
    description = "El dominio de disponibilidad donde se desplegará la instancia" 
    type        = string
}

variable "ubuntu_2204_image_ocid" {
    description = "El OCID de la imagen de Ubuntu 22.04" 
    type        = string
}

variable "ssh_public_key_content" {
    # ¡CORREGIDO! Cambiado de ssh_public_key a ssh_public_key_content
    description = "El contenido RAW de la clave pública SSH para acceder a la instancia" 
    type        = string
}