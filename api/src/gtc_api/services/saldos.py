from datetime import date
from sqlalchemy.orm import Session

from gtc_api.models.facturacion import (
    Contrato, Extracto, SaldoFactura, TipoTrxSaldo
)


def acumular_movimiento(db: Session, mov):
    """
    Acumula un movimiento en el saldo correspondiente del extracto abierto.
    """

    # 1. Obtener contrato
    contrato = db.query(Contrato).filter_by(id_contrato=mov.id_contrato).first()
    if not contrato:
        raise Exception(f"Contrato {mov.id_contrato} no existe")

    # 2. Obtener extracto abierto
    extracto = db.query(Extracto).filter_by(
        id_contrato=mov.id_contrato,
        num_extracto=contrato.extracto_abierto
    ).first()

    if not extracto:
        raise Exception(f"Extracto abierto no encontrado para contrato {mov.id_contrato}")

    # 3. Determinar tipo de saldo
    regla = db.query(TipoTrxSaldo).filter_by(
        tipo_movimiento=mov.tipo_movimiento
    ).first()

    if not regla:
        raise Exception(f"No existe regla tipo_trx_saldo para {mov.tipo_movimiento}")

    tipo_saldo = regla.tipo_saldo

    # 4. Buscar saldo del extracto
    saldo = db.query(SaldoFactura).filter_by(
        id_contrato=mov.id_contrato,
        num_extracto=extracto.num_extracto,
        tipo_saldo=tipo_saldo
    ).first()

    if not saldo:
        saldo = SaldoFactura(
            id_contrato=mov.id_contrato,
            num_extracto=extracto.num_extracto,
            tipo_saldo=tipo_saldo,
            saldo_acumulado=0,
            saldo_amortizado=0,
            saldo_diario={},
            aplicacion_pagos={}
        )
        db.add(saldo)

    # 5. Determinar signo
    importe = mov.importe
    if mov.signo == "H":  # Haber → resta saldo
        importe = -importe

    # 6. Acumular
    saldo.saldo_acumulado += importe

    # 7. Registrar saldo diario
    hoy = mov.fecha_contable.isoformat()
    saldo.saldo_diario[hoy] = float(saldo.saldo_acumulado - saldo.saldo_amortizado)

    # 8. Actualizar saldo disponible
    if contrato.saldo_disponible is not None:
        contrato.saldo_disponible -= importe  # si importe es negativo, suma

    db.commit()
    db.refresh(saldo)
    db.refresh(contrato)

    return saldo
