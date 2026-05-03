from gtc_api.db.session import SessionLocal
from gtc_api.models.param_general import ParamGeneral
from gtc_api.schemas.param_general import ParamGeneralCreate, ParamGeneralUpdate


def list_params():
    db = SessionLocal()
    try:
        return db.query(ParamGeneral).order_by(ParamGeneral.clave).all()
    finally:
        db.close()


def get_param(clave: str):
    db = SessionLocal()
    try:
        return (
            db.query(ParamGeneral)
            .filter(ParamGeneral.clave == clave)
            .one_or_none()
        )
    finally:
        db.close()


def set_param(payload: ParamGeneralCreate):
    db = SessionLocal()
    try:
        param = ParamGeneral(
            clave=payload.clave,
            valor=payload.valor,
        )
        db.add(param)
        db.commit()
        db.refresh(param)
        return param
    finally:
        db.close()


def update_param(clave: str, payload: ParamGeneralUpdate):
    db = SessionLocal()
    try:
        param = (
            db.query(ParamGeneral)
            .filter(ParamGeneral.clave == clave)
            .one_or_none()
        )
        if not param:
            return None

        param.valor = payload.valor
        db.commit()
        db.refresh(param)
        return param
    finally:
        db.close()
