from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gtc_api.db.session import SessionLocal
from gtc_api.schemas.movimientos import MovimientoCreate
from gtc_api.models.movimientos import MovimientoContrato
from gtc_api.services.saldos import acumular_movimiento

# ---------------------------
# Router principal de movimientos
# ---------------------------

router = APIRouter(tags=["Movimientos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/crear")
def crear_movimiento(mov: MovimientoCreate, db: Session = Depends(get_db)):
    nuevo = MovimientoContrato(**mov.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ---------------------------
# Router del simulador
# ---------------------------

sim_router = APIRouter(tags=["Simulador"])

@sim_router.post("/guardar")
async def guardar_movimiento(mov: MovimientoCreate):
    return {"status": "ok", "detalle": mov.dict()}

@sim_router.post("/procesar")
async def procesar_movimiento(mov: MovimientoCreate):
    resultado = {
        "evaluacion": "OK",
        "riesgo": "BAJO",
        "alertas": [],
        "detalle": mov.dict()
    }
    return {"resultado": resultado}

# ---------------------------
# Router de movimientos con integración a facturación
# ---------------------------
@router.post("/crear")
def crear_movimiento(mov: MovimientoCreate, db: Session = Depends(get_db)):
    nuevo = MovimientoContrato(**mov.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # Integración con facturación
    from gtc_api.services.saldos import acumular_movimiento
    acumular_movimiento(db, nuevo)

    return nuevo