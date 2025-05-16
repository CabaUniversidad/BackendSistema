from supabase import create_client
from src.config.settings import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_proveedores_supa():
    response = supabase.table("proveedores").select("*").execute()
    return response.data


def get_proveedor_supa(id):
    response = (
        supabase.table("proveedores")
        .select("*")
        .eq("idproveedor", id) 
        .execute()
    )
    return response.data
