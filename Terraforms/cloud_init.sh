#!/bin/bash
# Script simplificado de cloud-init para la VM de OCI.
# Objetivo: Instalar Docker y Docker Compose (plugin) en Ubuntu.

# 1. Instalar dependencias básicas
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release ufw

# 2. Instalar Docker
sudo mkdir -p /etc/apt/keyrings
…# 5. Configurar Firewall UFW (abrir puertos 22, 8080 y 80)
sudo ufw allow ssh
sudo ufw allow 80/tcp  # Para el frontend
sudo ufw allow 8080/tcp # Para el backend
sudo ufw --force enable

echo "Docker, Docker Compose y Firewall configurados correctamente."
