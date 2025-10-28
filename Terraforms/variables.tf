variable "tenancy_ocid" {
    description = "El OCID del arrendamiento (tenancy)" 
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

variable "private_key_path" {
    description = "La ruta al archivo de la clave privada API (oci_api_key.pem)" 
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
    description = "El contenido RAW de la clave pública SSH para acceder a la instancia" 
    type        = string
}