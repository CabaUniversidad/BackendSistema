from typing import List
from src.model.usuario_modelo import Usuario

# Lista que simula una base de datos temporal (en memoria)
lista_usuarios: List[Usuario] = []

def crear_usuario(usuario: Usuario) -> Usuario:
    lista_usuarios.append(usuario)
    return usuario

def obtener_usuarios() -> List[Usuario]:
    return lista_usuarios
