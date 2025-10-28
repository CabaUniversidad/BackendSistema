#!/bin/bash

# Este script instala Docker y Docker Compose V2 en la VM.

echo "--- 1. ACTUALIZAR SISTEMA E INSTALAR DEPENDENCIAS ---"
# Limpieza forzada de locks para evitar conflictos residuales de cloud-init
sudo rm -f /var/lib/dpkg/lock-frontend
sudo rm -f /var/lib/apt/lists/lock
sudo dpkg --configure -a

sudo apt update -y
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

echo "--- 2. INSTALAR DOCKER ENGINE (Método Oficial) ---"
# Añadir la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Configurar el repositorio estable
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# **ACTUALIZACIÓN CRÍTICA**: Actualizamos la lista de paquetes *después* de añadir el repositorio
sudo apt update -y 
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "--- 3. CONFIGURAR PERMISOS DE USUARIO ---"
# El usuario de SSH (ubuntu) debe poder usar Docker.
sudo usermod -aG docker ubuntu

echo "Instalación de Docker completada."