# test/unit/unit_proveedor.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Importa la aplicación FastAPI (ajusta la ruta si es necesario)
from src.main import app 

client = TestClient(app)

# --- Datos de prueba simulados ---
MOCK_PROVEEDOR_SINGLE = {
    "idproveedor": "PROV001",
    "nomproveedor": "Tech Supplies Inc.",
    "telefono": "555-1234",
    "email": "tech@supply.com"
}

MOCK_PROVEEDORES_DATA = [
    MOCK_PROVEEDOR_SINGLE,
    {
        "idproveedor": "PROV002",
        "nomproveedor": "Fashion Source Ltd.",
        "telefono": "555-5678",
        "email": "fashion@source.com"
    }
]

MOCK_PRODUCTOS_DE_PROVEEDOR = [
    {"idprod": "PROD001", "nomproducto": "Tornillo de 10mm"},
    {"idprod": "PROD002", "nomproducto": "Arandela G-5"}
]

# Excepción personalizada para simular errores de DB/Servicio
class DatabaseConnectionError(Exception):
    pass

# ID de proveedor para las pruebas
TEST_PROVEEDOR_ID = MOCK_PROVEEDOR_SINGLE["idproveedor"] 

# =========================================================================
# ENDPOINT 1: GET /proveedores (Todos los proveedores)
# =========================================================================

@patch("src.main.get_proveedores_service")
def test_get_all_proveedores_success(mock_get_proveedores_service):
    """Prueba que /proveedores retorne todos los datos (200 OK)."""
    
    # --- ENTRADA (MOCK) ---
    print("\n" + "=="*20)
    print("TEST: test_get_all_proveedores_success")
    mock_get_proveedores_service.return_value = MOCK_PROVEEDORES_DATA
    
    response = client.get("/proveedores")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON, size): {len(response.json())}")
    print("=="*20)

    assert response.status_code == 200
    assert len(response.json()) == 2


@patch("src.main.get_proveedores_service")
def test_get_all_proveedores_propagates_error(mock_get_proveedores_service):
    """Prueba que la excepción se propague si el servicio falla."""
    
    # --- ENTRADA (MOCK) ---
    EXCEPTION_DETAIL = "Fallo de conexión en /proveedores"
    mock_get_proveedores_service.side_effect = DatabaseConnectionError(EXCEPTION_DETAIL)
    
    print("\n" + "=="*20)
    print("TEST: test_get_all_proveedores_propagates_error")
    
    # AFIRMACIÓN de excepción
    with pytest.raises(DatabaseConnectionError) as excinfo:
        client.get("/proveedores")
    
    # --- SALIDA (EXCEPCIÓN CAPTURADA) ---
    print(f"OUTPUT (Captured Exception): {excinfo.type.__name__}: {excinfo.value}")
    print("=="*20)

    assert EXCEPTION_DETAIL in str(excinfo.value)

# =========================================================================
# ENDPOINT 2: GET /proveedores/by_id (Proveedor único por ID)
# =========================================================================

@patch("src.main.get_proveedor_service")
def test_get_proveedor_by_id_success(mock_get_proveedor_service):
    """Prueba el éxito al buscar un proveedor por ID (200 OK)."""
    
    # --- ENTRADA (MOCK) ---
    print("\n" + "=="*20)
    print("TEST: test_get_proveedor_by_id_success")
    mock_get_proveedor_service.return_value = MOCK_PROVEEDOR_SINGLE
    
    response = client.get(f"/proveedores/by_id?id={TEST_PROVEEDOR_ID}")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response ID): {response.json().get('idproveedor')}")
    print("=="*20)

    assert response.status_code == 200
    assert response.json()["idproveedor"] == TEST_PROVEEDOR_ID
    mock_get_proveedor_service.assert_called_once_with(TEST_PROVEEDOR_ID)


@patch("src.main.get_proveedor_service")
def test_get_proveedor_by_id_not_found(mock_get_proveedor_service):
    """Prueba el caso de proveedor no encontrado (404 NOT FOUND)."""
    
    # --- ENTRADA (MOCK) ---
    NON_EXISTENT_ID = "PROV999"
    print("\n" + "=="*20)
    print("TEST: test_get_proveedor_by_id_not_found")
    mock_get_proveedor_service.return_value = None # Simula que no se encontró en la DB
    
    response = client.get(f"/proveedores/by_id?id={NON_EXISTENT_ID}")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON): {response.json()}")
    print("=="*20)

    assert response.status_code == 404
    assert response.json() == {}
    mock_get_proveedor_service.assert_called_once_with(NON_EXISTENT_ID)


@patch("src.main.get_proveedor_service")
def test_get_proveedor_by_id_id_too_long(mock_get_proveedor_service):
    """Prueba la validación de FastAPI: ID de longitud máxima violada (422)."""
    
    INVALID_ID = "PROV001X" # Longitud 8, max es 7
    
    # --- ENTRADA ---
    print("\n" + "=="*20)
    print("TEST: test_get_proveedor_by_id_id_too_long")
    print(f"INPUT (ID): {INVALID_ID} (Longitud > 7)")
    
    response = client.get(f"/proveedores/by_id?id={INVALID_ID}")
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Error Type): {response.json().get('detail')[0].get('type')}")
    print("=="*20)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_too_long"
    mock_get_proveedor_service.assert_not_called()

# =========================================================================
# ENDPOINT 3: GET /proveedores/producto/by_idpv (Productos de un proveedor)
# =========================================================================

@patch("src.main.get_producto_proveedor_service")
def test_get_productos_proveedor_success(mock_get_producto_proveedor_service):
    """Prueba que la ruta de productos por proveedor retorne datos (200 OK)."""
    
    # --- ENTRADA (MOCK) ---
    print("\n" + "=="*20)
    print("TEST: test_get_productos_proveedor_success")
    mock_get_producto_proveedor_service.return_value = MOCK_PRODUCTOS_DE_PROVEEDOR
    
    response = client.get(f"/proveedores/producto/by_idpv?id={TEST_PROVEEDOR_ID}")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Products count): {len(response.json())}")
    print("=="*20)

    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_get_producto_proveedor_service.assert_called_once_with(TEST_PROVEEDOR_ID)


@patch("src.main.get_producto_proveedor_service")
def test_get_productos_proveedor_not_found(mock_get_producto_proveedor_service):
    """Prueba que la ruta de productos por proveedor retorne 404 si está vacía."""
    
    # --- ENTRADA (MOCK) ---
    print("\n" + "=="*20)
    print("TEST: test_get_productos_proveedor_not_found")
    mock_get_producto_proveedor_service.return_value = [] # Lista vacía
    
    response = client.get(f"/proveedores/producto/by_idpv?id={TEST_PROVEEDOR_ID}")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON): {response.json()}")
    print("=="*20)

    assert response.status_code == 404
    assert response.json()["message"] == "No se encontraron productos para ese proveedor."


@patch("src.main.get_producto_proveedor_service")
def test_get_productos_proveedor_missing_id(mock_get_producto_proveedor_service):
    """Prueba que el parámetro 'id' sea requerido (422)."""
    
    # --- ENTRADA ---
    print("\n" + "=="*20)
    print("TEST: test_get_productos_proveedor_missing_id")
    
    response = client.get("/proveedores/producto/by_idpv")
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print("=="*20)

    assert response.status_code == 422
    mock_get_producto_proveedor_service.assert_not_called()