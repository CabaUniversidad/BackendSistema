#!/bin/bash

# Actualizar el sistema e instalar dependencias
sudo apt update -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Instalar Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update -y
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Instalar Docker Compose (v2)
sudo apt install -y docker-compose-plugin

# Añadir el usuario 'ubuntu' (o el usuario de la VM) al grupo docker para evitar usar sudo
sudo usermod -aG docker ubuntu 

# Establecer la hora de la zona horaria a UTC (opcional, pero buena práctica)
sudo timedatectl set-timezone UTC

# Opcional: Limpieza
sudo apt autoremove -y

echo "Docker y Docker Compose instalados y configurados."