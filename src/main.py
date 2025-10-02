from fastapi import FastAPI ,WebSocket
from src.model.usuario_modelo import Usuario

from src.services.usuario_servicio import crear_usuario,obtener_usuarios,lista_usuarios
import asyncio
app = FastAPI(
    title="API de Usuarios",
    description="Una API básica para registrar y listar usuarios.",
    version="1.0.0"
) 
usuarioActual=0
@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        if usuarioActual!=len(lista_usuarios):
            usuarioActual=len(lista_usuarios) 
            
            await ws.send_text(lista_usuarios[-1]) 
            await asyncio.sleep(2) 
            


@app.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    return crear_usuario(usuario)

@app.get("/usuarios", response_model=list[Usuario])
def listar_usuarios():
    return obtener_usuarios()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
