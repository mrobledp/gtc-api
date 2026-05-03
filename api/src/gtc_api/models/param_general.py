from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ParamGeneral(Base):
    __tablename__ = "param_general"
    __table_args__ = {"schema": "gtc"}

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(100), unique=True, nullable=False)
    valor = Column(String(500), nullable=False)
    fecha_insercion = Column(DateTime, server_default=func.now(), nullable=False)
    fecha_actualiza = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
