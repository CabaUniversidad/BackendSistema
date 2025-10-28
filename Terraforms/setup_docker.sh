#!/bin/bash

# Este script instala Docker y Docker Compose V2 en la VM.

echo "--- 1. ACTUALIZAR SISTEMA E INSTALAR DEPENDENCIAS ---"
sudo apt update -y
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

echo "--- 2. INSTALAR DOCKER ENGINE (Método Oficial) ---"
# Añadir la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Configurar el repositorio estable
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine y Docker Compose V2 Plugin
sudo apt update -y
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "--- 3. CONFIGURAR PERMISOS DE USUARIO ---"
# El usuario de SSH (ubuntu) debe poder usar Docker. Esto requiere sudo.
sudo usermod -aG docker ubuntu

echo "--- 4. ESPERAR Y VERIFICAR ---"
# Esperamos un momento para que el servicio Docker se levante completamente.
sleep 10
sudo docker info

echo "Instalación de Docker completada."