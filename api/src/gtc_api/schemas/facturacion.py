from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Any, Dict


# ============================================
# 1. Paramétrica: tipo_trx_saldo
# ============================================

class TipoTrxSaldoCreate(BaseModel):
    tipo_movimiento: str
    tipo_saldo: str
    descripcion: Optional[str] = None
    activo: bool = True


class TipoTrxSaldoRead(BaseModel):
    tipo_movimiento: str
    tipo_saldo: str
    descripcion: Optional[str]
    activo: bool
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]

    model_config = {"from_attributes": True}


# ============================================
# 2. Paramétrica: param_saldo
# ============================================

class ParamSaldoCreate(BaseModel):
    tipo_saldo: str
    descripcion: Optional[str] = None
    interes_anual: float
    forma_calculo: str
    pct_pago_minimo: float
    comisiones: Optional[Dict[str, Any]] = None
    gastos: Optional[Dict[str, Any]] = None
    activo: bool = True


class ParamSaldoRead(BaseModel):
    tipo_saldo: str
    descripcion: Optional[str]
    interes_anual: float
    forma_calculo: str
    pct_pago_minimo: float
    comisiones: Optional[Dict[str, Any]]
    gastos: Optional[Dict[str, Any]]
    activo: bool
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]

    model_config = {"from_attributes": True}


# ============================================
# 3. Tabla de acumulación: saldos_factura
# ============================================

class SaldoFacturaRead(BaseModel):
    id_contrato: str
    num_extracto: int
    tipo_saldo: str
    saldo_acumulado: float
    saldo_amortizado: float
    saldo_diario: Optional[Dict[str, float]]
    aplicacion_pagos: Optional[Dict[str, Any]]
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]

    model_config = {"from_attributes": True}


# ============================================
# 4. Tabla de pagos: pagos_contrato
# ============================================

class PagoContratoCreate(BaseModel):
    id_contrato: str
    num_extracto: int
    fecha_pago: date
    importe_pago: float
    metodo_pago: Optional[str] = None
    referencia_externa: Optional[str] = None
    detalle_aplicacion: Optional[Dict[str, Any]] = None


class PagoContratoRead(BaseModel):
    id_pago: int
    id_contrato: str
    num_extracto: int
    fecha_pago: date
    importe_pago: float
    metodo_pago: Optional[str]
    referencia_externa: Optional[str]
    detalle_aplicacion: Optional[Dict[str, Any]]
    creado_en: Optional[datetime]

    model_config = {"from_attributes": True}


# ============================================
# 5. Tabla de extractos
# ============================================

class ExtractoCreate(BaseModel):
    id_contrato: str
    num_extracto: int
    fecha_apertura: date
    fecha_cierre: Optional[date] = None
    estado: str = "ABIERTO"


class ExtractoRead(BaseModel):
    id_contrato: str
    num_extracto: int
    fecha_apertura: date
    fecha_cierre: Optional[date]
    estado: str
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]

    model_config = {"from_attributes": True}


# ============================================
# 6. Tabla de contratos
# ============================================

class ContratoCreate(BaseModel):
    id_contrato: str
    extracto_abierto: int = 1
    limite_credito: Optional[float] = None
    saldo_disponible: Optional[float] = None
    estado: str = "ACTIVO"


class ContratoUpdate(BaseModel):
    extracto_abierto: Optional[int] = None
    limite_credito: Optional[float] = None
    saldo_disponible: Optional[float] = None
    estado: Optional[str] = None


class ContratoRead(BaseModel):
    id_contrato: str
    extracto_abierto: int
    limite_credito: Optional[float]
    saldo_disponible: Optional[float]
    estado: str
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]

    model_config = {"from_attributes": True}
