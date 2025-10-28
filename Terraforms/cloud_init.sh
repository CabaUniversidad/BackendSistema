#!/bin/bash

# --- 1. ACTUALIZAR SISTEMA ---
sudo apt update -y

# --- 2. INSTALAR UFW y CONFIGURAR PUERTOS (Esencial para la seguridad) ---
sudo apt install -y ufw
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3000/tcp
sudo ufw allow 8000/tcp
sudo ufw --force enable

echo "Configuración inicial de la VM completada (sin Docker)."