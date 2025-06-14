from fastapi import FastAPI,status, Path, Query, APIRouter
from fastapi.responses import PlainTextResponse,JSONResponse
from src.supabase_service import get_proveedores_service,get_proveedor_service,get_producto_proveedor_service

app = FastAPI()



@app.get("/",tags=['Home'])
def home():
    return PlainTextResponse(content="hola mundo",status_code=200) 

@app.get("/proveedores",tags=['Proveedor'])
def get_proveedor():
    return JSONResponse(content=get_proveedores_service())
@app.get("/proveedores/by_id", tags=["Proveedor"])  # ruta retorna por id
def get_proveedor(id: str = Query(max_length=4,min_length=4)) ->  dict:
    if get_proveedor_service(id):
        return JSONResponse(content=get_proveedor_service(id), status_code=200)
    return JSONResponse(content={}, status_code=404)
@app.get("/proveedores/producto/by_idpv", tags=["Proveedor"]) # retorna todos lo productos de un proveedor segun su ipPROVEEDOR
def get_productos_proveedor(id: str = Query(..., max_length=4, min_length=4)) -> JSONResponse:
    productos = get_producto_proveedor_service(id)
    if productos:
        return JSONResponse(content=productos, status_code=200)
    return JSONResponse(content={"message": "No se encontraron productos para ese proveedor."}, status_code=404)

