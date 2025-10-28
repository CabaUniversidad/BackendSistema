from pydantic import BaseModel

class EmpleadoEditarRequest(BaseModel):
    Nombres: str
    Apellidos: str
    Usuario: str
    Password: str
    Estado: str
    Telefono: str
    Email: str  # ← sin validación de formato
    Rol: str
