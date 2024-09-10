from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


class B3Data(Base):
    __tablename__ = "b3_data"

    id = Column(Integer, primary_key=True, index=True)
    setor = Column(String, index=True)
    codigo = Column(String)
    acao = Column(String)
    tipo = Column(String)
    quantidade_teorica = Column(Integer)
    porcentagem_participacao = Column(Float)
    porcentagem_participacao_acumulada = Column(Float)
    data_pregao = Column(Date)
