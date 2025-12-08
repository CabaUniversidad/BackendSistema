# test/unit/unit_producto.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.main import app 

client = TestClient(app)

# --- Datos de prueba simulados ---
MOCK_PRODUCTO_SINGLE = {
    "idprod": "PROD001", 
    "nomproducto": "Laptop A", 
    "idcategoria": 1,
    "stock": 50,
    "codbarras": 12345
}

MOCK_PRODUCTOS_DATA = [
    MOCK_PRODUCTO_SINGLE,
    {
        "idprod": "PROD002", 
        "nomproducto": "Teclado Mecánico", 
        "idcategoria": 1,
        "stock": 100,
        "codbarras": 54321
    },
    {"idprod": "PROD003", "nomproducto": "Mouse Gamer", "idcategoria": 1, "stock": 200, "codbarras": 67890}
]

# Excepción personalizada para simular errores de DB/Servicio
class DatabaseConnectionError(Exception):
    pass

# =========================================================================
# ENDPOINT: GET /Productos (Todos los productos)
# =========================================================================

@patch("src.main.get_productos_service")
def test_get_all_productos_success(mock_get_productos_service):
    """Prueba que el endpoint /Productos retorne todos los datos (200 OK)."""
    
    # --- ENTRADA (MOCK) ---
    print("\n" + "=="*20)
    print("TEST: test_get_all_productos_success")
    print(f"INPUT (Mocked data size): {len(MOCK_PRODUCTOS_DATA)}")
    mock_get_productos_service.return_value = MOCK_PRODUCTOS_DATA
    
    response = client.get("/Productos")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON, size): {len(response.json())}")
    print("=="*20)

    assert response.status_code == 200
    assert len(response.json()) == 3


@patch("src.main.get_productos_service")
def test_get_all_productos_empty(mock_get_productos_service):
    """Prueba que el endpoint /Productos retorne lista vacía (200 OK)."""
    
    # --- ENTRADA (MOCK) ---
    print("\n" + "=="*20)
    print("TEST: test_get_all_productos_empty")
    mock_get_productos_service.return_value = []
    
    response = client.get("/Productos")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON): {response.json()}")
    print("=="*20)

    assert response.status_code == 200
    assert response.json() == []


@patch("src.main.get_productos_service")
def test_get_all_productos_propagates_error(mock_get_productos_service):
    """Prueba que la excepción del servicio se propague."""
    
    # --- ENTRADA (MOCK) ---
    EXCEPTION_DETAIL = "Fallo de conexión en /Productos"
    mock_get_productos_service.side_effect = DatabaseConnectionError(EXCEPTION_DETAIL)
    
    print("\n" + "=="*20)
    print("TEST: test_get_all_productos_propagates_error")
    print(f"INPUT (Mocked Error): {DatabaseConnectionError.__name__}: {EXCEPTION_DETAIL}")
    
    # AFIRMACIÓN de excepción
    with pytest.raises(DatabaseConnectionError) as excinfo:
        client.get("/Productos")
    
    # --- SALIDA (EXCEPCIÓN CAPTURADA) ---
    print(f"OUTPUT (Captured Exception): {excinfo.type.__name__}: {excinfo.value}")
    print("=="*20)

    assert EXCEPTION_DETAIL in str(excinfo.value)

# =========================================================================
# ENDPOINT: GET /productos/by_categoria?id=int (Casos límite)
# =========================================================================

# NOTA: Los tests de éxito (200), no encontrado (404), y propagación de error 
# se asumen cubiertos por las pruebas iniciales. Aquí solo incluimos los casos límite solicitados.

@patch("src.main.get_productos_por_categoria_service")
def test_productos_by_categoria_missing_id(mock_get_productos_service):
    """Prueba la validación automática de FastAPI cuando el parámetro 'id' falta (422)."""
    
    # --- ENTRADA ---
    print("\n" + "=="*20)
    print("TEST: test_productos_by_categoria_missing_id")
    
    response = client.get("/productos/by_categoria")
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Error Type): {response.json().get('detail')[0].get('type')}")
    print("=="*20)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    mock_get_productos_service.assert_not_called()


@patch("src.main.get_productos_por_categoria_service")
def test_productos_by_categoria_invalid_type(mock_get_productos_service):
    """Prueba la validación de tipo de FastAPI cuando 'id' no es un entero (422)."""
    
    INVALID_ID = "abc"
    
    # --- ENTRADA ---
    print("\n" + "=="*20)
    print("TEST: test_productos_by_categoria_invalid_type")
    print(f"INPUT (Category ID): {INVALID_ID}")
    
    response = client.get(f"/productos/by_categoria?id={INVALID_ID}")
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Error Type): {response.json().get('detail')[0].get('type')}")
    print("=="*20)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"
    mock_get_productos_service.assert_not_called()


@patch("src.main.get_productos_por_categoria_service")
def test_productos_by_categoria_service_returns_none(mock_get_productos_service):
    """Prueba defensiva: verifica que si el servicio devuelve None, el endpoint devuelva 404."""
    
    # --- ENTRADA ---
    TEST_DEFENSIVE_ID = 500 
    print("\n" + "=="*20)
    print("TEST: test_productos_by_categoria_service_returns_none")
    print("INPUT (Mocked return): None")
    
    mock_get_productos_service.return_value = None

    response = client.get(f"/productos/by_categoria?id={TEST_DEFENSIVE_ID}")

    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON): {response.json()}")
    print("=="*20)
    
    assert response.status_code == 404
    assert response.json()["message"] == "No se encontraron productos para esa categoría."


# =========================================================================
# ENDPOINT: GET /productos/by_codbarras?codbarras=int
# =========================================================================

@patch("src.main.get_producto_por_codbarras_service")
def test_get_producto_by_codbarras_success(mock_get_producto_service):
    """Prueba el éxito al buscar por código de barras (200 OK)."""
    
    # --- ENTRADA (MOCK) ---
    TEST_BARCODE = MOCK_PRODUCTO_SINGLE["codbarras"]
    print("\n" + "=="*20)
    print("TEST: test_get_producto_by_codbarras_success")
    print(f"INPUT (Barcode): {TEST_BARCODE}")
    mock_get_producto_service.return_value = MOCK_PRODUCTO_SINGLE
    
    response = client.get(f"/productos/by_codbarras?codbarras={TEST_BARCODE}")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON ID): {response.json().get('idprod')}")
    print("=="*20)

    assert response.status_code == 200
    assert response.json()["codbarras"] == TEST_BARCODE
    mock_get_producto_service.assert_called_once_with(TEST_BARCODE)


@patch("src.main.get_producto_por_codbarras_service")
def test_get_producto_by_codbarras_not_found(mock_get_producto_service):
    """Prueba el caso de producto no encontrado (404 NOT FOUND)."""
    
    # --- ENTRADA (MOCK) ---
    TEST_BARCODE = 11111
    print("\n" + "=="*20)
    print("TEST: test_get_producto_by_codbarras_not_found")
    mock_get_producto_service.return_value = None # Simula que no se encontró en la DB
    
    response = client.get(f"/productos/by_codbarras?codbarras={TEST_BARCODE}")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON): {response.json()}")
    print("=="*20)

    assert response.status_code == 404
    assert response.json() == {"message": "Producto no encontrado."}
    mock_get_producto_service.assert_called_once_with(TEST_BARCODE)


@patch("src.main.get_producto_por_codbarras_service")
def test_get_producto_by_codbarras_invalid_type(mock_get_producto_service):
    """Prueba la validación de tipo de FastAPI cuando 'codbarras' no es un entero (422)."""
    
    INVALID_BARCODE = "codigo_invalido"
    
    # --- ENTRADA ---
    print("\n" + "=="*20)
    print("TEST: test_get_producto_by_codbarras_invalid_type")
    print(f"INPUT (Barcode): {INVALID_BARCODE}")
    
    response = client.get(f"/productos/by_codbarras?codbarras={INVALID_BARCODE}")
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Error Type): {response.json().get('detail')[0].get('type')}")
    print("=="*20)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"
    mock_get_producto_service.assert_not_called()


@patch("src.main.get_producto_por_codbarras_service")
def test_get_producto_by_codbarras_propagates_error(mock_get_producto_service):
    """Prueba que la excepción del servicio se propague en caso de fallo de DB."""
    
    # --- ENTRADA (MOCK) ---
    TEST_BARCODE = 98765
    EXCEPTION_DETAIL = "Fallo de RPC al buscar por barras"
    mock_get_producto_service.side_effect = DatabaseConnectionError(EXCEPTION_DETAIL)
    
    print("\n" + "=="*20)
    print("TEST: test_get_producto_by_codbarras_propagates_error")
    
    # AFIRMACIÓN de excepción
    with pytest.raises(DatabaseConnectionError) as excinfo:
        client.get(f"/productos/by_codbarras?codbarras={TEST_BARCODE}")
    
    # --- SALIDA (EXCEPCIÓN CAPTURADA) ---
    print(f"OUTPUT (Captured Exception): {excinfo.type.__name__}: {excinfo.value}")
    print("=="*20)

    assert EXCEPTION_DETAIL in str(excinfo.value)