from pydantic import BaseModel

class Proveedor(BaseModel):
    idproveedor: str
    nomproveedor: str | None = None
    telefono: str | None = None
    email: str | None = None
    imgproveedor: str | None = None
