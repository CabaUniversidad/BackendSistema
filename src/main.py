from fastapi import FastAPI,status, Path, Query, APIRouter,HTTPException
from fastapi.responses import PlainTextResponse,JSONResponse
from src.model.EmpleadoEditarRequest import EmpleadoEditarRequest
from src.services.supabase_service import get_proveedores_service,get_proveedor_service,get_producto_proveedor_service,get_usuarios_service,editar_empleado_service,get_categorias_service,get_productos_por_categoria_service,get_productos_service,get_rols_service,get_estado_empleado_service,get_producto_por_codbarras_service

app = FastAPI()



@app.get("/",tags=['Home'])
def home():
    return PlainTextResponse(content="hola mundo",status_code=200) 
#---------categoria--------------------
@app.get("/categorias",tags=['Categoria'])
def get_categorias():
    return JSONResponse(content=get_categorias_service())

#---------producto--------------------
@app.get("/productos/by_categoria", tags=["Producto"])
def get_productos_por_categoria(id: int = Query(...)) -> JSONResponse:
    productos = get_productos_por_categoria_service(id)
    if productos:
        return JSONResponse(content=productos, status_code=200)
    return JSONResponse(content={"message": "No se encontraron productos para esa categoría."}, status_code=404)
@app.get("/Productos",tags=['Producto'])
def get_Productos():
    return JSONResponse(content=get_productos_service())

@app.get("/productos/by_codbarras", tags=["Producto"])
def get_producto_por_codbarras(codbarras: int = Query(...)) -> JSONResponse:
    producto = get_producto_por_codbarras_service(codbarras)
    if producto:
        return JSONResponse(content=producto, status_code=200)
    return JSONResponse(content={"message": "Producto no encontrado."}, status_code=404)







#-----------proveedor-------------
@app.get("/proveedores",tags=['Proveedor'])
def get_proveedors():
    return JSONResponse(content=get_proveedores_service())

@app.get("/proveedores/by_id", tags=["Proveedor"])  # ruta retorna por id
def get_proveedor(id: str = Query(max_length=7,min_length=7)) ->  dict:
    if get_proveedor_service(id):
        return JSONResponse(content=get_proveedor_service(id), status_code=200)
    return JSONResponse(content={}, status_code=404)

@app.get("/proveedores/producto/by_idpv", tags=["Proveedor"])
def get_productos_proveedor(id: str = Query(..., max_length=7, min_length=7)) -> JSONResponse:
    productos = get_producto_proveedor_service(id)
    if productos:
        return JSONResponse(content=productos, status_code=200)
    return JSONResponse(content={"message": "No se encontraron productos para ese proveedor."}, status_code=404)





#------------empleado-------------
@app.get("/empleados", tags=["Empleado"]) # retorna todos lo productos de un proveedor segun su ipPROVEEDOR
def get_usuarios() -> JSONResponse:
    usuario = get_usuarios_service()
    if usuario:
        return JSONResponse(content=usuario, status_code=200)
    return JSONResponse(content={"message": "No se encontraron usuarios."}, status_code=404)
@app.get("/empleado/rol",tags=['Empleado'])
def get_rols():
    return JSONResponse(content=get_rols_service())
@app.get("/empleado/estado",tags=['Empleado'])
def get_estado_empleado():
    return JSONResponse(content=get_estado_empleado_service())
@app.put("/empleados/{cod_empleado}", tags=["Empleado"])
def editar_empleado(cod_empleado: str, request: EmpleadoEditarRequest):
    try:
        data = request.dict()
        data["CodEmpleado"] = cod_empleado
        result = editar_empleado_service(data)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        print("ERROR al editar empleado:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
