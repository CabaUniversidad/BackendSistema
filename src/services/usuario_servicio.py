# src/services/usuario_servicio.py
import sqlite3
from datetime import datetime
from typing import List, Optional
from src.model.usuario_modelo import Usuario

base_sqlite="src/data/usuarios.db" 
# --- Crear tabla ---
def crear_tabla():
    conexion = sqlite3.connect(base_sqlite)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fecha_registro TEXT NOT NULL,
            activo INTEGER NOT NULL,
            rol TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# --- Crear usuario ---
def crear_usuario(usuario: Usuario) -> Usuario:
    crear_tabla()
    conexion = sqlite3.connect(base_sqlite)
    cursor = conexion.cursor()

    # --- Verificar si ya existe el correo ---
    cursor.execute("SELECT id FROM usuarios WHERE correo = ?", (usuario.correo,))
    if cursor.fetchone():
        conexion.close()
        raise ValueError("El correo ya está registrado")

    cursor.execute("""
        INSERT INTO usuarios (nombre, correo, password, fecha_registro, activo, rol)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        usuario.nombre,
        usuario.correo,
        usuario.password,
        usuario.fecha_registro.isoformat(),
        int(usuario.activo),
        usuario.rol
    ))
    conexion.commit()
    usuario.id = cursor.lastrowid
    conexion.close()
    return usuario


# --- Obtener todos los usuarios ---
def obtener_usuarios() -> List[Usuario]:
    crear_tabla()
    conexion = sqlite3.connect(base_sqlite)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, correo, password, fecha_registro, activo, rol FROM usuarios")
    filas = cursor.fetchall()
    conexion.close()
    usuarios = [Usuario(
        id=f[0],
        nombre=f[1],
        correo=f[2],
        password=f[3],
        fecha_registro=datetime.fromisoformat(f[4]),
        activo=bool(f[5]),
        rol=f[6]
    ) for f in filas]
    return usuarios

# --- Obtener usuario por id ---
def obtener_usuario_por_id(user_id: int) -> Optional[Usuario]:
    crear_tabla()
    conexion = sqlite3.connect(base_sqlite)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, correo, password, fecha_registro, activo, rol FROM usuarios WHERE id = ?", (user_id,))
    fila = cursor.fetchone()
    conexion.close()
    if fila:
        return Usuario(
            id=fila[0],
            nombre=fila[1],
            correo=fila[2],
            password=fila[3],
            fecha_registro=datetime.fromisoformat(fila[4]),
            activo=bool(fila[5]),
            rol=fila[6]
        )
    return None

# --- Actualizar usuario ---
def actualizar_usuario(user_id: int, usuario: Usuario) -> Optional[Usuario]:
    crear_tabla()
    conexion = sqlite3.connect(base_sqlite)
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nombre = ?, correo = ?, password = ?, activo = ?, rol = ?
        WHERE id = ?
    """, (
        usuario.nombre,
        usuario.correo,
        usuario.password,
        int(usuario.activo),
        usuario.rol,
        user_id
    ))
    conexion.commit()
    conexion.close()
    return obtener_usuario_por_id(user_id)

# --- Eliminar usuario ---
def eliminar_usuario(user_id: int) -> bool:
    crear_tabla()
    conexion = sqlite3.connect(base_sqlite)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()
    return filas_afectadas > 0