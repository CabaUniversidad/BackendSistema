from typing import List
from src.model.usuario_modelo import Usuario

# Lista que simula una base de datos temporal (en memoria)
usuarios: List[Usuario] = []

def crear_usuario(usuario: Usuario) -> Usuario:
    usuarios.append(usuario)
    return usuario

def obtener_usuarios() -> List[Usuario]:
    return usuarios
