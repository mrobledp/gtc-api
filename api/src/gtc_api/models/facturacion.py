from sqlalchemy import (
    Column, String, Integer, Date, DateTime, Numeric, Boolean, JSON, BigInteger
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# ============================================
# 1. Paramétrica: tipo_trx_saldo
# ============================================

class TipoTrxSaldo(Base):
    __tablename__ = "tipo_trx_saldo"
    __table_args__ = {"schema": "gtc"}

    tipo_movimiento = Column(String(50), primary_key=True)
    tipo_saldo = Column(String(50), nullable=False)
    descripcion = Column(String(255))
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================
# 2. Paramétrica: param_saldo
# ============================================

class ParamSaldo(Base):
    __tablename__ = "param_saldo"
    __table_args__ = {"schema": "gtc"}

    tipo_saldo = Column(String(50), primary_key=True)
    descripcion = Column(String(255))
    interes_anual = Column(Numeric(5, 2), nullable=False)
    forma_calculo = Column(String(50), nullable=False)
    pct_pago_minimo = Column(Numeric(5, 2), nullable=False)
    comisiones = Column(JSON)
    gastos = Column(JSON)
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================
# 3. Tabla de acumulación: saldos_factura
# ============================================

class SaldoFactura(Base):
    __tablename__ = "saldos_factura"
    __table_args__ = {"schema": "gtc"}

    id_contrato = Column(String(50), primary_key=True)
    num_extracto = Column(Integer, primary_key=True)
    tipo_saldo = Column(String(50), primary_key=True)

    saldo_acumulado = Column(Numeric(18, 2), nullable=False, default=0)
    saldo_amortizado = Column(Numeric(18, 2), nullable=False, default=0)
    saldo_diario = Column(JSON)
    aplicacion_pagos = Column(JSON)

    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================
# 4. Tabla de pagos: pagos_contrato
# ============================================

class PagoContrato(Base):
    __tablename__ = "pagos_contrato"
    __table_args__ = {"schema": "gtc"}

    id_pago = Column(BigInteger, primary_key=True, autoincrement=True)
    id_contrato = Column(String(50), nullable=False)
    num_extracto = Column(Integer, nullable=False)
    fecha_pago = Column(Date, nullable=False)
    importe_pago = Column(Numeric(18, 2), nullable=False)
    metodo_pago = Column(String(50))
    referencia_externa = Column(String(100))
    detalle_aplicacion = Column(JSON)
    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)


# ============================================
# 5. Tabla de extractos
# ============================================

class Extracto(Base):
    __tablename__ = "extractos"
    __table_args__ = {"schema": "gtc"}

    id_contrato = Column(String(50), primary_key=True)
    num_extracto = Column(Integer, primary_key=True)
    fecha_apertura = Column(Date, nullable=False)
    fecha_cierre = Column(Date)
    estado = Column(String(30), nullable=False)
    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================
# 6. Tabla de contratos
# ============================================

class Contrato(Base):
    __tablename__ = "contratos"
    __table_args__ = {"schema": "gtc"}

    id_contrato = Column(String(50), primary_key=True)
    extracto_abierto = Column(Integer, nullable=False)
    limite_credito = Column(Numeric(18, 2))
    saldo_disponible = Column(Numeric(18, 2))
    estado = Column(String(30), nullable=False)
    creado_en = Column(DateTime, nullable=False, default=datetime.utcnow)
    actualizado_en = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
