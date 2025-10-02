from fastapi import FastAPI ,WebSocket
from src.model.usuario_modelo import Usuario
from src.services import usuario_servicio
import asyncio
app = FastAPI(
    title="API de Usuarios",
    description="Una API básica para registrar y listar usuarios.",
    version="1.0.0"
)
@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    contador = 0
    while True:
        contador += 1
        await ws.send_text(f"Mensaje {contador}")  # mando texto
        await asyncio.sleep(3)  # espero 3 segundos



@app.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    return usuario_servicio.crear_usuario(usuario)

@app.get("/usuarios", response_model=list[Usuario])
def listar_usuarios():
    return usuario_servicio.obtener_usuarios()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
