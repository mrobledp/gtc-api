from pydantic import BaseModel
from datetime import datetime

class ParamGeneralBase(BaseModel):
    clave: str
    valor: str

class ParamGeneralCreate(ParamGeneralBase):
    pass

class ParamGeneralUpdate(BaseModel):
    valor: str

class ParamGeneralOut(ParamGeneralBase):
    id: int
    fecha_insercion: datetime
    fecha_actualiza: datetime

    class Config:
        orm_mode = True
