from fastapi import FastAPI 
from src.model.usuario_modelo import Usuario
from src.services import usuario_servicio

app = FastAPI(
    title="API de Usuarios",
    description="Una API básica para registrar y listar usuarios.",
    version="1.0.0"
)

@app.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    return usuario_servicio.crear_usuario(usuario)

@app.get("/usuarios", response_model=list[Usuario])
def listar_usuarios():
    return usuario_servicio.obtener_usuarios()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
