# src/main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from src.model.usuario_modelo import Usuario
from src.services.usuario_servicio import crear_usuario, obtener_usuarios, obtener_usuario_por_id, actualizar_usuario, eliminar_usuario

app = FastAPI()

# Obtener la IP pública (establecida por el pipeline/docker-compose)
IP_PUBLICA = os.getenv("VM_IP", "0.0.0.0") 

# --- CORRECCIÓN CRÍTICA DE CORS ---
origins = [
    # 1. Acceso interno de contenedor a contenedor (Flet al Backend)
    # CRÍTICO: El nombre del servicio 'backend' se resuelve a la IP interna de ese contenedor.
    "http://backend:8000",
    
    # 2. Acceso externo desde el navegador (necesario si la API se accede directamente)
    # Se utiliza la IP pública de la VM y el puerto 80 (ya que el frontend está en el puerto 80 externo)
    f"http://{IP_PUBLICA}", 
    
    # 3. Acceso local (para desarrollo)
    "http://localhost:8550", 
    
    # 4. Asegurar la IP específica que viste en tu error, por si acaso
    "http://64.181.166.239", 
]
# --- FIN DE CORRECCIÓN CRÍTICA DE CORS ---


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Por simplicidad de despliegue, usamos * aquí. Se recomienda usar la lista 'origins' en producción.
    # allow_origins=origins, # Puedes descomentar esto y borrar la línea anterior si quieres más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/usuarios")
def crear_usuario_nuevo(usuario: Usuario):
    usuario.fecha_registro = datetime.now()
    try:
        return crear_usuario(usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/usuarios_get")
def listar_usuarios():
    return obtener_usuarios()

@app.get("/usuarios/{user_id}")
def obtener_usuario(user_id: int):
    usuario = obtener_usuario_por_id(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{user_id}")
def actualizar_usuario_endpoint(user_id: int, usuario: Usuario):
    usuario_actualizado = actualizar_usuario(user_id, usuario)
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_actualizado

@app.delete("/usuarios/{user_id}")
def eliminar_usuario_endpoint(user_id: int):
    exito = eliminar_usuario(user_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"} 
if __name__ == "__main__":
    import uvicorn
    import os

    # Escuchar en 0.0.0.0 para que sea accesible desde otros contenedores
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEV_MODE") == "1"
    )
