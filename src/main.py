from fastapi import FastAPI
from src.model.usuario_modelo import Usuario
from src.services.usuario_servicio import crear_usuario, obtener_usuarios

app = FastAPI(
    title="API de Usuarios",
    description="Una API básica para registrar y listar usuarios.",
    version="1.0.0"
)

# Endpoints
@app.post("/usuarios", response_model=Usuario)
def crear_usuario_nuevo(usuario: Usuario):
    return crear_usuario(usuario)

@app.get("/usuarios_get", response_model=list[Usuario])
def listar_usuarios():
    return obtener_usuarios()


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
