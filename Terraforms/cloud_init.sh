#!/bin/bash

# --- 1. ACTUALIZAR SISTEMA E INSTALAR DEPENDENCIAS ---
sudo apt update -y
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# --- 2. INSTALAR DOCKER ENGINE (Método Oficial) ---

# Añadir la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Configurar el repositorio estable
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine y Docker Compose V2 Plugin
sudo apt update -y
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# --- 3. CONFIGURAR PERMISOS DE USUARIO ---
# Añadir el usuario 'ubuntu' al grupo docker.
# (Aunque la activación requiere un nuevo login, lo hacemos por si acaso y usamos sudo en el pipeline)
sudo usermod -aG docker ubuntu

# --- 4. CONFIGURAR FIREWALL (UFW) ---
# Instalar e inicializar UFW (si es necesario)
sudo apt install -y ufw
# Abre puertos para SSH, HTTP, 8000 (FastAPI), 3000 (Front), etc.
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3000/tcp
sudo ufw allow 8000/tcp
# Habilita el firewall (si no está activo)
sudo ufw --force enable

echo "Configuración de la VM completada: Docker instalado, UFW configurado."