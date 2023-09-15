from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Cor(Base):
    __tablename__ = 'cor'

    id = Column("pk_cor", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    hex = Column(String(7), unique=True )
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, hex:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Cor

        Arguments:
            nome: nome da cor
            hex: valor hex da cor
            data_insercao: data de quando o produto foi inserido à base
        """
        self.nome = nome
        self.hex = hex

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
