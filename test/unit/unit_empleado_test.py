# test/unit/unit_empleado.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.main import app 

client = TestClient(app)

# Excepción personalizada para simular errores de DB/Servicio
class DatabaseConnectionError(Exception):
    pass

# --- Datos de prueba simulados ---
MOCK_EMPLEADO_ADMIN = [{
    "idempleado": "EMP001", 
    "usuario": "admin_user", 
    "es_admin": True,
    "rol": "Administrador",
    "estado": "Activo"
}]

MOCK_EMPLEADO_NON_ADMIN = [{
    "idempleado": "EMP002", 
    "usuario": "regular_user", 
    "es_admin": False,
    "rol": "Vendedor",
    "estado": "Activo"
}]

MOCK_EMPLEADOS_DATA = MOCK_EMPLEADO_ADMIN + MOCK_EMPLEADO_NON_ADMIN

MOCK_ROLES = [{"idrol": 1, "nomrol": "Administrador"}, {"idrol": 2, "nomrol": "Vendedor"}]
MOCK_ESTADOS = [{"idestado": 1, "nomestado": "Activo"}, {"idestado": 2, "nomestado": "Inactivo"}]
TEST_COD_EMPLEADO = MOCK_EMPLEADO_ADMIN[0]["idempleado"]

# PAYLOAD COMPLETO para las pruebas PUT (CORRECCIÓN del error 422)
COMPLETE_EDIT_PAYLOAD = {
    # Estos campos son necesarios para que el modelo EmpleadoEditarRequest pase la validación de Pydantic
    "Nombres": "Admin Nuevo",
    "Apellidos": "Test Apellido",
    "Usuario": "admin_test",
    "Password": "NewPassword123",
    "Estado": "Activo",
    "Telefono": "1234567",
    "Email": "admin@example.com",
    "Rol": "Administrador" 
}


# =========================================================================
# ENDPOINT: POST /login
# =========================================================================

@patch("src.main.login_empleado_service")
def test_login_success_admin(mock_login_service):
    """Prueba de login exitoso con credenciales de administrador (success: True)."""
    
    # --- ENTRADA (MOCK) ---
    LOGIN_PAYLOAD = {"usuario": "admin_user", "password": "securepassword"}
    print("\n" + "=="*20)
    print("TEST: test_login_success_admin")
    mock_login_service.return_value = MOCK_EMPLEADO_ADMIN
    
    response = client.post("/login", json=LOGIN_PAYLOAD)
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Success flag): {response.json().get('success')}")
    print("=="*20)

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["idempleado"] == "EMP001"
    mock_login_service.assert_called_once_with(LOGIN_PAYLOAD["usuario"], LOGIN_PAYLOAD["password"])


@patch("src.main.login_empleado_service")
def test_login_success_non_admin(mock_login_service):
    """Prueba de login exitoso con usuario regular (success: False)."""
    
    # --- ENTRADA (MOCK) ---
    LOGIN_PAYLOAD = {"usuario": "regular_user", "password": "userpassword"}
    print("\n" + "=="*20)
    print("TEST: test_login_success_non_admin")
    mock_login_service.return_value = MOCK_EMPLEADO_NON_ADMIN
    
    response = client.post("/login", json=LOGIN_PAYLOAD)
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Success flag): {response.json().get('success')}")
    print("=="*20)

    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["data"]["idempleado"] == "EMP002"


@patch("src.main.login_empleado_service")
def test_login_failure(mock_login_service):
    """Prueba de login fallido (usuario/contraseña incorrectos), debe ser 401."""
    
    # --- ENTRADA (MOCK) ---
    LOGIN_PAYLOAD = {"usuario": "bad_user", "password": "wrong_password"}
    print("\n" + "=="*20)
    print("TEST: test_login_failure")
    mock_login_service.return_value = [] 
    
    response = client.post("/login", json=LOGIN_PAYLOAD)
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Detail): {response.json().get('detail')}")
    print("=="*20)

    assert response.status_code == 401
    assert "Usuario o contraseña incorrectos" in response.json()["detail"]


def test_login_validation_missing_field():
    """Prueba de validación de FastAPI: Falta un campo requerido (422)."""
    
    # --- ENTRADA ---
    print("\n" + "=="*20)
    print("TEST: test_login_validation_missing_field")
    
    response = client.post("/login", json={"usuario": "test_user"})
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Error Type): {response.json().get('detail')[0].get('type')}")
    print("=="*20)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"


# =========================================================================
# ENDPOINT: GET /empleados
# =========================================================================

@patch("src.main.get_usuarios_service")
def test_get_all_empleados_success(mock_get_usuarios_service):
    """Prueba que el endpoint /empleados retorne datos (200 OK)."""
    
    # --- ENTRADA (MOCK) ---
    print("\n" + "=="*20)
    print("TEST: test_get_all_empleados_success")
    mock_get_usuarios_service.return_value = MOCK_EMPLEADOS_DATA
    
    response = client.get("/empleados")
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON, size): {len(response.json())}")
    print("=="*20)

    assert response.status_code == 200
    assert len(response.json()) == 2


@patch("src.main.get_usuarios_service")
def test_get_all_empleados_not_found(mock_get_usuarios_service):
    """Prueba que el endpoint /empleados retorne 404 si la lista está vacía."""
    
    # --- ENTRADA (MOCK) ---
    print("\n" + "=="*20)
    print("TEST: test_get_all_empleados_not_found")
    mock_get_usuarios_service.return_value = []
    
    response = client.get("/empleados")
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON): {response.json()}")
    print("=="*20)

    assert response.status_code == 404
    assert response.json()["message"] == "No se encontraron usuarios."


# =========================================================================
# ENDPOINT: GET /empleado/rol & GET /empleado/estado
# =========================================================================

@patch("src.main.get_rols_service")
def test_get_rols_success(mock_get_rols_service):
    """Prueba de éxito para /empleado/rol (200 OK)."""
    
    print("\n" + "=="*20)
    print("TEST: test_get_rols_success")
    mock_get_rols_service.return_value = MOCK_ROLES
    
    response = client.get("/empleado/rol")
    
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON, size): {len(response.json())}")
    print("=="*20)

    assert response.status_code == 200
    assert len(response.json()) == 2

@patch("src.main.get_estado_empleado_service")
def test_get_estado_empleado_success(mock_get_estado_empleado_service):
    """Prueba de éxito para /empleado/estado (200 OK)."""
    
    print("\n" + "=="*20)
    print("TEST: test_get_estado_empleado_success")
    mock_get_estado_empleado_service.return_value = MOCK_ESTADOS
    
    response = client.get("/empleado/estado")
    
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON, size): {len(response.json())}")
    print("=="*20)

    assert response.status_code == 200
    assert len(response.json()) == 2
    
# =========================================================================
# ENDPOINT: PUT /empleados/{cod_empleado}
# =========================================================================

@patch("src.main.editar_empleado_service")
def test_editar_empleado_success(mock_editar_empleado_service):
    """Prueba de edición exitosa (200 OK) usando el payload completo."""
    
    # --- ENTRADA ---
    EDIT_PAYLOAD = COMPLETE_EDIT_PAYLOAD # <<< USANDO PAYLOAD COMPLETO
    EDIT_RESULT = {"message": "Empleado EMP001 actualizado correctamente", "count": 1}
    
    print("\n" + "=="*20)
    print("TEST: test_editar_empleado_success")
    mock_editar_empleado_service.return_value = EDIT_RESULT
    
    response = client.put(f"/empleados/{TEST_COD_EMPLEADO}", json=EDIT_PAYLOAD)
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Response JSON): {response.json()}")
    print("=="*20)

    assert response.status_code == 200
    assert "actualizado correctamente" in response.json()["message"]
    
    expected_data = EDIT_PAYLOAD.copy()
    expected_data["CodEmpleado"] = TEST_COD_EMPLEADO
    mock_editar_empleado_service.assert_called_once_with(expected_data)


@patch("src.main.editar_empleado_service")
def test_editar_empleado_service_error_400(mock_editar_empleado_service):
    """Prueba de error de servicio capturado por el try/except del endpoint (400 Bad Request)."""
    
    # --- ENTRADA ---
    EDIT_PAYLOAD = COMPLETE_EDIT_PAYLOAD # <<< USANDO PAYLOAD COMPLETO
    ERROR_MSG = "No se pudo conectar a la base de datos."
    
    print("\n" + "=="*20)
    print("TEST: test_editar_empleado_service_error_400")
    # El servicio levanta una excepción
    mock_editar_empleado_service.side_effect = DatabaseConnectionError(ERROR_MSG)
    
    response = client.put(f"/empleados/{TEST_COD_EMPLEADO}", json=EDIT_PAYLOAD)
    
    # --- SALIDA ---
    print(f"OUTPUT (Response Status): {response.status_code}")
    print(f"OUTPUT (Detail): {response.json().get('detail')}")
    print("=="*20)

    assert response.status_code == 400
    assert ERROR_MSG in response.json()["detail"]