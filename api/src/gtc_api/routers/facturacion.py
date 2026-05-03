from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from gtc_api.db.session import SessionLocal

from gtc_api.models.facturacion import (
    TipoTrxSaldo, ParamSaldo, Contrato, Extracto,
    PagoContrato, SaldoFactura
)

from gtc_api.schemas.facturacion import (
    TipoTrxSaldoCreate, TipoTrxSaldoRead,
    ParamSaldoCreate, ParamSaldoRead,
    ContratoCreate, ContratoRead, ContratoUpdate,
    ExtractoCreate, ExtractoRead,
    PagoContratoCreate, PagoContratoRead,
    SaldoFacturaRead
)

from gtc_api.services.pagos import aplicar_pago
from gtc_api.services.extractos import cerrar_extracto


router = APIRouter(tags=["Facturación"])


# ---------------------------
# Dependencia DB
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# 1. PARAMÉTRICAS
# ---------------------------

@router.post("/tipo-trx-saldo", response_model=TipoTrxSaldoRead)
def crear_tipo_trx_saldo(data: TipoTrxSaldoCreate, db: Session = Depends(get_db)):
    nuevo = TipoTrxSaldo(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/tipo-trx-saldo", response_model=list[TipoTrxSaldoRead])
def listar_tipo_trx_saldo(db: Session = Depends(get_db)):
    return db.query(TipoTrxSaldo).all()


@router.post("/param-saldo", response_model=ParamSaldoRead)
def crear_param_saldo(data: ParamSaldoCreate, db: Session = Depends(get_db)):
    nuevo = ParamSaldo(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/param-saldo", response_model=list[ParamSaldoRead])
def listar_param_saldo(db: Session = Depends(get_db)):
    return db.query(ParamSaldo).all()


# ---------------------------
# 2. CONTRATOS
# ---------------------------

@router.post("/contratos", response_model=ContratoRead)
def crear_contrato(data: ContratoCreate, db: Session = Depends(get_db)):
    nuevo = Contrato(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/contratos", response_model=list[ContratoRead])
def listar_contratos(db: Session = Depends(get_db)):
    return db.query(Contrato).all()


@router.get("/contratos/{id_contrato}", response_model=ContratoRead)
def obtener_contrato(id_contrato: str, db: Session = Depends(get_db)):
    contrato = db.query(Contrato).filter_by(id_contrato=id_contrato).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return contrato


# ---------------------------
# 3. EXTRACTOS
# ---------------------------

@router.post("/extractos", response_model=ExtractoRead)
def crear_extracto(data: ExtractoCreate, db: Session = Depends(get_db)):
    nuevo = Extracto(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/extractos/{id_contrato}", response_model=list[ExtractoRead])
def listar_extractos(id_contrato: str, db: Session = Depends(get_db)):
    return db.query(Extracto).filter_by(id_contrato=id_contrato).all()


# ---------------------------
# 4. PAGOS
# ---------------------------

@router.post("/pagos", response_model=PagoContratoRead)
def registrar_pago(data: PagoContratoCreate, db: Session = Depends(get_db)):
    nuevo = PagoContrato(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/pagos/{id_contrato}/{num_extracto}", response_model=list[PagoContratoRead])
def listar_pagos(id_contrato: str, num_extracto: int, db: Session = Depends(get_db)):
    return (
        db.query(PagoContrato)
        .filter_by(id_contrato=id_contrato, num_extracto=num_extracto)
        .all()
    )


# ---------------------------
# 5. SALDOS
# ---------------------------

@router.get("/saldos/{id_contrato}/{num_extracto}", response_model=list[SaldoFacturaRead])
def obtener_saldos(id_contrato: str, num_extracto: int, db: Session = Depends(get_db)):
    return (
        db.query(SaldoFactura)
        .filter_by(id_contrato=id_contrato, num_extracto=num_extracto)
        .all()
    )


# ---------------------------
# 6. PAGOS - APLICACIÓN
# ---------------------------

@router.post("/pagos", response_model=PagoContratoRead)
def registrar_pago(data: PagoContratoCreate, db: Session = Depends(get_db)):
    nuevo = PagoContrato(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # Aplicar pago a los saldos
    aplicar_pago(db, nuevo)

    db.refresh(nuevo)
    return nuevo


# ---------------------------
# 7. EXTRACTOS - CIERRE Y GENERACIÓN DE SALDOS
# ---------------------------

@router.post("/extractos/{id_contrato}/cerrar")
def cerrar_extracto_api(id_contrato: str, db: Session = Depends(get_db)):
    resultado = cerrar_extracto(db, id_contrato)
    return resultado

