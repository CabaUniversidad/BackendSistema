# test/unit/unit_categoria.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.main import app 

client = TestClient(app)

# --- Datos de prueba simulados ---
MOCK_CATEGORIAS_DATA = [
    {"idcategoria": 1, "nomcategoria": "Electrónica"},
    {"idcategoria": 2, "nomcategoria": "Ropa"},
    {"idcategoria": 3, "nomcategoria": "Hogar"}
]

# Excepción personalizada para simular errores de DB
class DatabaseConnectionError(Exception):
    pass

# =========================================================================
# PRUEBA 1: ÉXITO (Código 200)
# =========================================================================
@patch("src.main.get_categorias_service")
def test_get_categorias_success(mock_get_categorias_service):
    
    # --- ENTRADA (MOCK) ---
    print("\n" + "="*40)
    print("TEST: test_get_categorias_success")
    print(f"INPUT (Mocked data): {MOCK_CATEGORIAS_DATA}")
    mock_get_categorias_service.return_value = MOCK_CATEGORIAS_DATA
    
    # Llamada al endpoint
    response = client.get("/categorias")
    
    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON): {response.json()}")
    print("="*40)

    # AFIRMACIONES
    assert response.status_code == 200
    assert response.json() == MOCK_CATEGORIAS_DATA

# =========================================================================
# PRUEBA 2: CONTENIDO VACÍO (Código 200)
# =========================================================================
@patch("src.main.get_categorias_service")
def test_get_categorias_no_content(mock_get_categorias_service):
    
    # --- ENTRADA (MOCK) ---
    MOCK_EMPTY_DATA = []
    print("\n" + "="*40)
    print("TEST: test_get_categorias_no_content")
    print(f"INPUT (Mocked data): {MOCK_EMPTY_DATA}")
    mock_get_categorias_service.return_value = MOCK_EMPTY_DATA

    # Llamada al endpoint
    response = client.get("/categorias")

    # --- SALIDA (RESPUESTA) ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON): {response.json()}")
    print("="*40)
    
    # AFIRMACIONES
    assert response.status_code == 200
    assert response.json() == []

# =========================================================================
# PRUEBA 3: ERROR INTERNO (Comprueba la propagación de la excepción)
# =========================================================================
@patch("src.main.get_categorias_service")
def test_get_categorias_propagates_error(mock_get_categorias_service):
    """
    Verifica que la excepción del servicio se propague.
    """
    # --- ENTRADA (MOCK) ---
    EXCEPTION_DETAIL = "Fallo de conexión simulado"
    mock_get_categorias_service.side_effect = DatabaseConnectionError(EXCEPTION_DETAIL)
    
    print("\n" + "="*40)
    print("TEST: test_get_categorias_propagates_error")
    print(f"INPUT (Mocked Error): {DatabaseConnectionError.__name__}: {EXCEPTION_DETAIL}")
    
    # Llamada y AFIRMACIÓN de excepción
    # Usamos 'as excinfo' para capturar la información de la excepción
    with pytest.raises(DatabaseConnectionError) as excinfo:
        client.get("/categorias")
    
    # --- SALIDA (EXCEPCIÓN CAPTURADA) ---
    print(f"OUTPUT (Captured Exception): {excinfo.type.__name__}: {excinfo.value}")
    print("="*40)

    # AFIRMACIONES
    assert EXCEPTION_DETAIL in str(excinfo.value)
    
    # =========================================================================
# PRUEBA 4: VALIDACIÓN DE ESQUEMA
# =========================================================================
@patch("src.main.get_categorias_service")
def test_get_categorias_schema_validation(mock_get_categorias_service):
    """
    Verifica que la respuesta devuelta por el endpoint contenga los campos esperados.
    """
    mock_get_categorias_service.return_value = MOCK_CATEGORIAS_DATA
    response = client.get("/categorias")
    
    # Afirma que la respuesta es una lista no vacía
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    
    # Verifica el esquema del primer elemento
    first_item = response.json()[0]
    
    # Afirma que las claves esperadas están presentes
    assert "idcategoria" in first_item
    assert "nomcategoria" in first_item
    
    # Opcional: Verificar el tipo de datos (FastAPI/Pydantic se encargaría de esto,
    # pero es una buena práctica de test)
    assert isinstance(first_item["idcategoria"], int)
    assert isinstance(first_item["nomcategoria"], str)
    
    
    # =========================================================================
# PRUEBA 5: PRUEBA DE VOLUMEN (High Volume Test)
# =========================================================================
@patch("src.main.get_categorias_service")
def test_get_categorias_high_volume(mock_get_categorias_service):
    """
    Prueba que el endpoint maneje un gran número de registros.
    """
    
    # Simulamos 1000 categorías
    large_data = [{"idcategoria": i, "nomcategoria": f"Categoria {i}"} for i in range(1, 1001)]
    
    mock_get_categorias_service.return_value = large_data
    
    response = client.get("/categorias")
    
    # Afirmaciones
    assert response.status_code == 200
    
    # Verifica que se hayan devuelto los 1000 elementos
    assert len(response.json()) == 1000
    
    # Verifica que el último elemento sea correcto
    assert response.json()[-1]["idcategoria"] == 1000
    assert response.json()[-1]["nomcategoria"] == "Categoria 1000"