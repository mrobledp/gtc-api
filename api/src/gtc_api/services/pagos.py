from datetime import date
from sqlalchemy.orm import Session

from gtc_api.models.facturacion import (
    Contrato, Extracto, SaldoFactura, PagoContrato
)


def aplicar_pago(db: Session, pago: PagoContrato):
    """
    Aplica un pago a los saldos del extracto abierto.
    """

    # 1. Obtener contrato
    contrato = db.query(Contrato).filter_by(id_contrato=pago.id_contrato).first()
    if not contrato:
        raise Exception(f"Contrato {pago.id_contrato} no existe")

    # 2. Obtener extracto abierto
    extracto = db.query(Extracto).filter_by(
        id_contrato=pago.id_contrato,
        num_extracto=pago.num_extracto
    ).first()

    if not extracto:
        raise Exception(f"Extracto {pago.num_extracto} no existe para contrato {pago.id_contrato}")

    # 3. Obtener todos los saldos del extracto
    saldos = (
        db.query(SaldoFactura)
        .filter_by(id_contrato=pago.id_contrato, num_extracto=pago.num_extracto)
        .all()
    )

    # Orden de amortización estándar
    orden = [
        "INTERESES",
        "COMISIONES",
        "GASTOS",
        "COMPRAS",
        "DISPOSICIONES",
        "OTROS"
    ]

    # Convertir a diccionario para acceso rápido
    saldos_dict = {s.tipo_saldo: s for s in saldos}

    restante = pago.importe_pago
    detalle = {}

    # 4. Aplicar pago según orden
    for tipo in orden:
        saldo = saldos_dict.get(tipo)
        if not saldo:
            continue

        if restante <= 0:
            break

        amortizable = min(restante, float(saldo.saldo_acumulado - saldo.saldo_amortizado))
        if amortizable > 0:
            saldo.saldo_amortizado += amortizable
            restante -= amortizable
            detalle[tipo] = amortizable

            # Actualizar saldo diario
            hoy = pago.fecha_pago.isoformat()
            saldo.saldo_diario[hoy] = float(saldo.saldo_acumulado - saldo.saldo_amortizado)

    # 5. Actualizar saldo disponible del contrato
    if contrato.saldo_disponible is not None:
        contrato.saldo_disponible += pago.importe_pago

    # 6. Guardar detalle de aplicación
    pago.detalle_aplicacion = detalle

    db.commit()

    return detalle
