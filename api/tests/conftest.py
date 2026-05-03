import json
import pytest
from fastapi.testclient import TestClient
from gtc_api.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def movement_cases():
    with open("tests/data/movements_cases.json", "r", encoding="utf-8") as f:
        return json.load(f)
