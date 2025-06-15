from supabase import create_client
from src.config.settings import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_proveedores_service():
    response = supabase.table("proveedores").select("*").execute()
    return response.data



def get_proveedor_service(id):
    response = supabase.table("proveedores").select("*").eq("idproveedor", id).execute()
    return response.data


def get_producto_proveedor_service(idproveedor: str):
    # Obtener todos los productos relacionados a un proveedor desde categoriaproveedor
    productos_ids_response = (
        supabase.from_("categoriaproveedor")
        .select("id_producto")
        .eq("idproveedor", idproveedor)
        .execute()
    )

    # Extraer solo la lista de IDs
    productos_ids = [p["id_producto"] for p in productos_ids_response.data]

    if not productos_ids:
        return []

    # Buscar los productos que estén en esa lista
    productos_response = (
        supabase.from_("productos_con_categoria")
        .select("*")
        .in_("id_producto", productos_ids)
        .execute()
    )

    return productos_response.data
#--------rol--------
def get_rol_service():
    response = supabase.table("rol").select("nomrol").execute()
    return response.data
#---------------ususarios-------------

def get_usuarios_service():
    response = supabase.rpc("obtener_usuarios_completos").execute()
    return response.data
def editar_empleado_service(data: dict):
    response = supabase.rpc("editar_empleado", {
        "p_cod_empleado": data["CodEmpleado"],
        "p_nombres": data["Nombres"],
        "p_apellidos": data["Apellidos"],
        "p_usuario": data["Usuario"],
        "p_password": data["Password"],
        "p_estado_nombre": data["Estado"],
        "p_telefono": data["Telefono"],
        "p_email": data["Email"],
        "p_rol_nombre": data["Rol"]
    }).execute()

    # Si la ejecución no lanza error, asumimos que se actualizó bien
    return {"message": "Empleado actualizado correctamente"}
