variable "tenancy_ocid" {
    description = "El OCID del arrendamiento (tenancy)" 
}

variable "user_ocid" {
    description = "El OCID del usuario" 
}

variable "fingerprint" {
    description = "La huella digital de la clave pública del usuario" 
}

variable "private_key_path" {
    description = "La ruta al archivo de la clave privada" 
}

variable "region" {
    description = "La región de Oracle Cloud" 
}

variable "compartment_ocid" {
    description = "El OCID del compartimiento" 
}

variable "subnet_id" {
    description = "El OCID de la subred" 
}

variable "availability_domain" {
    description = "El dominio de disponibilidad donde se desplegará la instancia" 
}

variable "ubuntu_2204_image_ocid" {
    description = "El OCID de la imagen de Ubuntu 22.04" 
}

variable "ssh_public_key" {
    description = "La clave pública SSH para acceder a la instancia" 
}
