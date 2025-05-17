from fastapi import FastAPI,status, Path, Query, APIRouter
from fastapi.responses import PlainTextResponse,JSONResponse
from src.services.supabase_service import get_proveedores_supa,get_proveedor_supa,get_productos_supa,get_Producto_categoriaproveedor_supa
app = FastAPI()



@app.get("/",tags=['Home'])
def home():
    return PlainTextResponse(content="hola mundo",status_code=200) 

@app.get("/proveedores",tags=['Proveedor'])
def get_proveedores():
    return JSONResponse(content=get_proveedores_supa())


@app.get("/proveedores/by_id", tags=["Proveedor"])  # ruta retorna por id
def get_proveedor(id: str = Query(max_length=4,min_length=4)) ->  dict:
    
    if get_proveedor_supa(id):
        return JSONResponse(content=get_proveedor_supa(id), status_code=200)
    return JSONResponse(content={}, status_code=404)
#----------productos De Proveedores-- -para CategoriaProveedor------
@app.get("/proveedor/productos/by_id", tags=["Proveedor"])  # ruta retorna por id
def get_producto(id: str = Query(max_length=4,min_length=4)) ->  dict:
    
    if get_Producto_categoriaproveedor_supa(id):
        return JSONResponse(content=get_Producto_categoriaproveedor_supa(id), status_code=200)
    return JSONResponse(content={}, status_code=404)

#----productos---
@app.get("/productos",tags=['Producto'])
def get_productos():
    return JSONResponse(content=get_productos_supa())





