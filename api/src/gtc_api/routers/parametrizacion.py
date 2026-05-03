from fastapi import APIRouter, HTTPException, status
from gtc_api.schemas.param_general import ParamGeneralCreate, ParamGeneralUpdate
from gtc_api.services.parm_manager import (
    list_params,
    get_param,
    set_param,
    update_param,
)

router = APIRouter(prefix="/parametros", tags=["Parámetros"])


# ============================
# GET: listar todos los parámetros
# ============================
@router.get("/")
def read_params():
    return list_params()


# ============================
# GET: obtener un parámetro por clave
# ============================
@router.get("/{clave}")
def read_param(clave: str):
    param = get_param(clave)
    if not param:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parámetro '{clave}' no encontrado",
        )
    return param


# ============================
# POST: crear parámetro
# ============================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_param(payload: ParamGeneralCreate):
    existing = get_param(payload.clave)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Parámetro '{payload.clave}' ya existe",
        )
    return set_param(payload)


# ============================
# PUT: actualizar parámetro
# ============================
@router.put("/{clave}")
def update_param_value(clave: str, payload: ParamGeneralUpdate):
    updated = update_param(clave, payload)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parámetro '{clave}' no encontrado",
        )
    return updated
