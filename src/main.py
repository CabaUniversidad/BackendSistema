from fastapi import FastAPI 
from src.model.usuario_modelo import Usuario

from src.services.usuario_servicio import crear_usuario,obtener_usuarios,lista_usuarios
import asyncio
app = FastAPI(
    title="API de Usuarios",
    description="Una API básica para registrar y listar usuarios.",
    version="1.0.0"
) 



@app.post("/usuarios", response_model=Usuario)
def crear_usuario_nuevo(usuario: Usuario):
    print(usuario)
    return crear_usuario(usuario)

@app.get("/usuarios_get", response_model=list[Usuario])
def listar_usuarios():
    return obtener_usuarios()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
