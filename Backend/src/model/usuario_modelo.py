from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class Usuario(BaseModel):
    id: Optional[int] = None  # Se asigna automáticamente en SQLite
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre del usuario")
    correo: EmailStr
    password: str = Field(..., min_length=6, description="Contraseña segura del usuario")
    fecha_registro: datetime = Field(default_factory=datetime.now)
    activo: bool = Field(default=True, description="Estado del usuario (activo/inactivo)")
    rol: str = Field(default="jugador", description="Rol: jugador, admin, etc.")

    # Validador personalizado para nombre
    @validator("nombre")
    def validar_nombre(cls, valor):
        if not valor.replace(" ", "").isalpha():
            raise ValueError("El nombre solo puede contener letras y espacios")
        return valor.title()

    # Validador personalizado para contraseña
    @validator("password")
    def validar_password(cls, valor):
        if len(valor) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        if not any(c.isdigit() for c in valor):
            raise ValueError("La contraseña debe contener al menos un número")
        if not any(c.isalpha() for c in valor):
            raise ValueError("La contraseña debe contener al menos una letra")
        return valor
