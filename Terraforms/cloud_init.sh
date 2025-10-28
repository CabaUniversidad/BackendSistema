#!/bin/bash
# Script robusto para cloud-init

# Asegurar que el PATH del root sea completo (incluyendo /usr/sbin)
export PATH=$PATH:/usr/sbin:/usr/bin:/sbin:/bin

# 1. Actualizar paquetes e instalar dependencias
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# 2. Instalar Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 3. Añadir el usuario 'ubuntu' al grupo docker
# La verificación de usuario es importante
if id -u ubuntu >/dev/null 2>&1; then
    # Usamos el path completo para usermod para mayor robustez
    sudo /usr/sbin/usermod -aG docker ubuntu
else
    echo "Usuario 'ubuntu' no encontrado."
fi

# 4. Habilitar y arrancar el servicio Docker
sudo systemctl enable docker
sudo systemctl start docker

echo "Docker y Docker Compose (plugin) instalados y listos."

# 5. Configurar UFW y abrir puerto 80 (HTTP)
sudo apt-get install -y ufw
sudo ufw allow ssh
sudo ufw allow http
sudo ufw --force enable

# ----------------------------------------------------
# 6. Crear y ejecutar el docker-compose.yml
# ----------------------------------------------------

DOCKER_COMPOSE_DIR="/home/ubuntu"
DOCKER_COMPOSE_FILE="$DOCKER_COMPOSE_DIR/docker-compose.yml"

mkdir -p $DOCKER_COMPOSE_DIR

# Crear el archivo YAML
cat <<EOF | sudo tee $DOCKER_COMPOSE_FILE
version: '3.8'

services:
  apache-web:
    image: httpd:latest
    container_name: apache_server
    restart: always
    ports:
      - "80:80"
EOF

# Asignar propiedad al usuario 'ubuntu'
sudo chown ubuntu:ubuntu $DOCKER_COMPOSE_FILE

# Ejecutar Docker Compose como el usuario 'ubuntu' desde el directorio correcto
cd $DOCKER_COMPOSE_DIR
sudo -u ubuntu docker compose up -d || sudo -u ubuntu docker-compose up -d

echo "Contenedor Apache levantado con Docker Compose."