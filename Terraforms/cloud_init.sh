#!/bin/bash

# Cloud-Init: Solo permisos, firewall y limpieza de locks.

# 1. Asegurarse de que no haya locks de apt pendientes (para evitar conflictos)
sudo rm -f /var/lib/dpkg/lock-frontend
sudo rm -f /var/lib/apt/lists/lock
sudo dpkg --configure -a

# 2. INSTALAR UFW y CONFIGURAR PUERTOS (Esencial para la seguridad)
# Si ufw no está instalado, apt lo instalará en este paso.
sudo apt install -y ufw

# Configuración del Firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3000/tcp
sudo ufw allow 8000/tcp
sudo ufw --force enable

echo "Configuración inicial de la VM completada (sin Docker)."