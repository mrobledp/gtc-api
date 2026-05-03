from sqlalchemy import Column, BigInteger, String, Date, DateTime, Numeric, CHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MovimientoContrato(Base):
    __tablename__ = "movimiento_contrato"
    __table_args__ = {"schema": "gtc"}

    id_movimiento = Column(BigInteger, primary_key=True, index=True)
    id_contrato = Column(String(50), nullable=False)
    fecha_operacion = Column(DateTime, nullable=False)
    fecha_contable = Column(Date, nullable=False)
    importe = Column(Numeric(18, 2), nullable=False)
    moneda = Column(CHAR(3), nullable=False)
    signo = Column(CHAR(1), nullable=False)
    tipo_movimiento = Column(String(50), nullable=False)
    descripcion = Column(String(255))
    comercio = Column(String(255))
    categoria = Column(String(100))
    codigo_autorizacion = Column(String(50))
    estado = Column(String(30), nullable=False)
    origen = Column(String(50))
    referencia_externa = Column(String(100))

INSERT_MOVIMIENTO = """
    INSERT INTO gtc.movimiento_contrato (
        id_contrato,
        fecha_operacion,
        fecha_contable,
        importe,
        moneda,
        signo,
        tipo_movimiento,
        descripcion,
        comercio,
        categoria,
        codigo_autorizacion,
        estado,
        origen,
        referencia_externa
    )
    VALUES (
        :id_contrato,
        :fecha_operacion,
        :fecha_contable,
        :importe,
        :moneda,
        :signo,
        :tipo_movimiento,
        :descripcion,
        :comercio,
        :categoria,
        :codigo_autorizacion,
        :estado,
        :origen,
        :referencia_externa
    )
    RETURNING id_movimiento;
"""
