import json
from fastapi.testclient import TestClient
from gtc_api.main import app
from pathlib import Path

client = TestClient(app)

def load_cases():
    BASE = Path(__file__).resolve().parent
    DATA = BASE / "data" / "movements_cases.json"

    print(f"Cargando casos de prueba desde: {DATA}")

    with open(DATA) as f:
        return json.load(f)

def test_create_movements():
    cases = load_cases()

    for case in cases:
        response = client.post("/movimientos/crear", json=case)
        assert response.status_code == 200, f"Error en caso: {case}"

        data = response.json()

        # Validamos que la API devuelve el movimiento creado
        for key in case:
            assert key in data, f"Falta el campo '{key}' en la respuesta"
            assert data[key] == case[key], f"Valor incorrecto en '{key}'"
