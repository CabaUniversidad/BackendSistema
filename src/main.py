from fastapi import FastAPI,status, Path, Query, APIRouter
from fastapi.responses import PlainTextResponse,JSONResponse
from src.services.supabase_service import get_proveedores
app = FastAPI()



@app.get("/",tags=['Home'])
def home():
    return PlainTextResponse(content="hola mundo",status_code=200) 

@app.get("/proveedores",tags=['Proveedor'])
def get_proveedor():
    return JSONResponse(content=get_proveedores())
@app.get("/proveedores/by_id", tags=["Proveedor"])  # ruta retorna por id
def get_movie(id: str = Query(max_length=4,min_length=4)) ->  dict:
    
    if get_proveedores(id):
        return JSONResponse(content=get_proveedores(id), status_code=200)
    return JSONResponse(content={}, status_code=404)




