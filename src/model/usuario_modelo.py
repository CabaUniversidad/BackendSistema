from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
