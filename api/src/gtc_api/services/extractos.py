from datetime import date
from sqlalchemy.orm import Session

from gtc_api.models.facturacion import (
    Contrato, Extracto, SaldoFactura, ParamSaldo
)


def cerrar_extracto(db: Session, id_contrato: str):
    """
    Cierra el extracto abierto de un contrato y abre uno nuevo.
    """

    # 1. Obtener contrato
    contrato = db.query(Contrato).filter_by(id_contrato=id_contrato).first()
    if not contrato:
        raise Exception(f"Contrato {id_contrato} no existe")

    num_extracto = contrato.extracto_abierto

    # 2. Obtener extracto abierto
    extracto = db.query(Extracto).filter_by(
        id_contrato=id_contrato,
        num_extracto=num_extracto
    ).first()

    if not extracto:
        raise Exception(f"Extracto {num_extracto} no existe para contrato {id_contrato}")

    if extracto.estado != "ABIERTO":
        raise Exception(f"El extracto {num_extracto} ya está cerrado")

    # 3. Obtener saldos del extracto
    saldos = (
        db.query(SaldoFactura)
        .filter_by(id_contrato=id_contrato, num_extracto=num_extracto)
        .all()
    )

    # 4. Calcular intereses (simplificado)
    for saldo in saldos:
        regla = db.query(ParamSaldo).filter_by(tipo_saldo=saldo.tipo_saldo).first()
        if not regla:
            continue

        interes_diario = float(regla.interes_anual) / 100 / 365

        # Interés simple sobre el saldo diario
        interes_total = 0
        if saldo.saldo_diario:
            for dia, valor in saldo.saldo_diario.items():
                interes_total += valor * interes_diario

        # Añadir intereses al saldo acumulado
        saldo.saldo_acumulado += interes_total

    # 5. Cerrar extracto
    extracto.estado = "CERRADO"
    extracto.fecha_cierre = date.today()

    # 6. Crear nuevo extracto
    nuevo_extracto = Extracto(
        id_contrato=id_contrato,
        num_extracto=num_extracto + 1,
        fecha_apertura=date.today(),
        estado="ABIERTO"
    )
    db.add(nuevo_extracto)

    # 7. Actualizar contrato
    contrato.extracto_abierto = num_extracto + 1

    db.commit()

    return {
        "extracto_cerrado": num_extracto,
        "nuevo_extracto": num_extracto + 1
    }
