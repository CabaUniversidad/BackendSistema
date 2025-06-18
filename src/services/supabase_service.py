from supabase import create_client
from src.config.settings import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_proveedores_service():
    response = supabase.table("proveedor").select("*").execute()
    return response.data

def get_proveedor_service(id):
    response = supabase.table("proveedor").select("*").eq("idproveedor", id).execute()
    return response.data


def get_producto_proveedor_service(idproveedor: str):
    response = supabase.rpc("get_productos_por_proveedor", {"proveedor_id": idproveedor}).execute()
    
    if not response.data:
        return []

    return response.data
def add_proveedor_service(data: dict):
    try:
        response = supabase.table("proveedor").insert(data).execute()
        return response.data  # ✅ forma correcta
    except Exception as e:
        raise Exception(f"Error al insertar proveedor: {e}")




def update_proveedor_service(idproveedor: str, data: dict):
    try:
        response = supabase.table("proveedor").update(data).eq("idproveedor", idproveedor).execute()
        return response.data
    except Exception as e:
        raise Exception(f"Error al actualizar proveedor: {e}")
#---------------ususarios-------------

def get_usuarios_service():
    response = supabase.rpc("obtener_usuarios_completos").execute()
    return response.data
def editar_empleado_service(data: dict):
    try:
        # Combinar nombres
        nombrecompleto = f"{data['Nombres']} {data['Apellidos']}"

        # Ejecutar RPC con nombres
        response = supabase.rpc("editar_empleado", {
            "p_cod_empleado": data["CodEmpleado"],
            "p_nombrecompleto": nombrecompleto,
            "p_usuario": data["Usuario"],
            "p_password": data["Password"],
            "p_estado_nombre": data["Estado"],
            "p_telefono": data["Telefono"],
            "p_email": data["Email"],
            "p_rol_nombre": data["Rol"]
        }).execute()
        
        return {"message": "Empleado actualizado correctamente"}
    except Exception as e:
        raise Exception(f"Error al actualizar empleado: {response}")
#_________________________tablas unidadas a empleado
def get_rols_service():
    response = supabase.table("rol").select("*").execute()
    return response.data
def get_estado_empleado_service():
    response = supabase.table("estadoemp").select("*").execute()
    return response.data

#----------productos---
def get_productos_service():
    response = supabase.rpc("get_productos_categoria").execute()
    return response.data
#----------categoria-----productos---
def get_categorias_service():
    response = supabase.table("categoria").select("*").execute()
    return response.data
def get_productos_por_categoria_service(idcategoria: int):
    response = supabase.rpc("get_productos_por_categoria", {"categoria_id": idcategoria}).execute()
    return response.data or []
def get_producto_por_codbarras_service(codbarras: int):
    response = supabase.rpc("get_producto_por_codbarras", {"p_codbarras": codbarras}).execute()
    return response.data or []
