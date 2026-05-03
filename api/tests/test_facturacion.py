import json
from fastapi.testclient import TestClient
from gtc_api.main import app

client = TestClient(app)


# ---------------------------
# 1. Paramétricas
# ---------------------------

def test_parametricas():
    # tipo_trx_saldo
    r = client.post("/facturacion/tipo-trx-saldo", json={
        "tipo_movimiento": "COMPRA",
        "tipo_saldo": "COMPRAS",
        "descripcion": "Compras normales"
    })
    assert r.status_code == 200

    # param_saldo
    r = client.post("/facturacion/param-saldo", json={
        "tipo_saldo": "COMPRAS",
        "interes_anual": 20.0,
        "forma_calculo": "365",
        "pct_pago_minimo": 5.0
    })
    assert r.status_code == 200


# ---------------------------
# 2. Contrato + Extracto
# ---------------------------

def test_crear_contrato_y_extracto():
    # Crear contrato
    r = client.post("/facturacion/contratos", json={
        "id_contrato": "C001",
        "extracto_abierto": 1,
        "limite_credito": 1000,
        "saldo_disponible": 1000
    })
    assert r.status_code == 200

    # Crear extracto 1
    r = client.post("/facturacion/extractos", json={
        "id_contrato": "C001",
        "num_extracto": 1,
        "fecha_apertura": "2024-01-01"
    })
    assert r.status_code == 200


# ---------------------------
# 3. Movimiento + Acumulación
# ---------------------------

def test_movimiento_acumula_saldo():
    movimiento = {
        "id_contrato": "C001",
        "fecha_operacion": "2024-01-10T10:00:00",
        "fecha_contable": "2024-01-10",
        "importe": 100.0,
        "moneda": "EUR",
        "signo": "D",
        "tipo_movimiento": "COMPRA"
    }

    r = client.post("/movimientos/crear", json=movimiento)
    assert r.status_code == 200

    # Verificar saldo acumulado
    r = client.get("/facturacion/saldos/C001/1")
    assert r.status_code == 200
    saldos = r.json()
    assert len(saldos) == 1
    assert saldos[0]["saldo_acumulado"] == 100.0

    # Verificar saldo disponible
    r = client.get("/facturacion/contratos/C001")
    contrato = r.json()
    assert contrato["saldo_disponible"] == 900.0


# ---------------------------
# 4. Pago + Amortización
# ---------------------------

def test_pago_amortiza_saldo():
    pago = {
        "id_contrato": "C001",
        "num_extracto": 1,
        "fecha_pago": "2024-01-15",
        "importe_pago": 50.0
    }

    r = client.post("/facturacion/pagos", json=pago)
    assert r.status_code == 200

    # Verificar amortización
    r = client.get("/facturacion/saldos/C001/1")
    saldo = r.json()[0]
    assert saldo["saldo_amortizado"] == 50.0

    # Verificar saldo disponible
    r = client.get("/facturacion/contratos/C001")
    contrato = r.json()
    assert contrato["saldo_disponible"] == 950.0


# ---------------------------
# 5. Cierre de extracto
# ---------------------------

def test_cierre_extracto():
    r = client.post("/facturacion/extractos/C001/cerrar")
    assert r.status_code == 200

    data = r.json()
    assert data["extracto_cerrado"] == 1
    assert data["nuevo_extracto"] == 2

    # Verificar que el extracto 2 existe
    r = client.get("/facturacion/extractos/C001")
    extractos = r.json()
    assert len(extractos) == 2
    assert extractos[1]["num_extracto"] == 2
    assert extractos[1]["estado"] == "ABIERTO"
