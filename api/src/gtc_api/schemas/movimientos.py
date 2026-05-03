from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class MovimientoCreate(BaseModel):
    id_contrato: str
    fecha_operacion: datetime
    fecha_contable: date
    importe: float
    moneda: str
    signo: str
    tipo_movimiento: str
    descripcion: Optional[str] = None
    comercio: Optional[str] = None
    categoria: Optional[str] = None
    codigo_autorizacion: Optional[str] = None
    estado: Optional[str] = "PENDIENTE"
    origen: Optional[str] = "SIMULADOR"
    referencia_externa: Optional[str] = None
