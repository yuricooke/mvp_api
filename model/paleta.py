from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Paleta(Base):
    __tablename__ = 'paleta'

    id = Column("pk_paleta", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    neutral = Column(String(7))
    primary = Column(String(7))
    accent = Column(String(7))

    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, neutral:str, primary: str,
                 accent: str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Cor

        Arguments:
            nome: nome da cor
            hex: valor hex da cor
            data_insercao: data de quando o produto foi inserido à base
        """
        self.nome = nome
        self.neutral = neutral
        self.primary = primary
        self.accent = accent


        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
