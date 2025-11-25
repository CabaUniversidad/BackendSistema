from unittest.mock import patch
from src.main import crear_usuario,listar_usuarios
import json


def test_unit_crear_usuario():
    dato_nuevo={
    "id": 1,
    "nombre": "Juan Pérez",
    "correo": "juan.perez@example.com",
    "password": "hashed_password_123",
    "fecha_registro": "2025-01-10T14:32:00",
    "activo": 1,
    "rol": "admin"
  }
def test_unit_create_categoria_logic():
    nombre_Cat = "categoria unitaria" 
    with patch("src.services.usuario_servicio.obtener_usuarios",return_value=MOCK_DB_dATA.copy()) as mock_load, patch(
        "app.crud.crear_usuario"
    ) as mock_save:
        resultado = crear_usuario(nombre_Cat)
        assert resultado == {
            "id": 11,
            "nombre": nombre_Cat,
        }  # incrementobasado en MOCK_DB_DATA
        mock_save.assert_called_once()
        datos_guardados = mock_save.call_args[0][0]
        print("\nDatos guardados en el mock:\n", json.dumps(datos_guardados, indent=4))
        print("---------------------------------------------------")
        assert any(
            cat for cat in datos_guardados["categorias"] if cat["nombre"] == nombre_Cat
        )