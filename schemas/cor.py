from pydantic import BaseModel
from typing import Optional, List
from model.cor import Cor



class CorSchema(BaseModel):
    """ Define como uma nova cor a ser inserida deve ser representada
    """
    nome: str = "Vermelho"
    hex: str = "#FF0000"


class CorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da cor.
    """
    nome: str = "Vermelho"
    id: int = 1
    

class ListagemCoresSchema(BaseModel):
    """ Define como uma listagem de cores será retornada.
    """
    cores:List[CorSchema]


def apresenta_cores(cores: List[Cor]):
    """ Retorna uma representação da cor seguindo o schema definido em
        CorViewSchema.
    """
    result = []
    for cor in cores:
        result.append({
            "nome": cor.nome,
            "hex": cor.hex,
        })

    return {"cores": result}


class CorViewSchema(BaseModel):
    """ Define como uma cor será retornada: nome + cor.
    """
    id: int = 1
    nome: str = "Vermelho"
    hex: str = "#FF0000"


class CorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_cor(cor: Cor):
    """ Retorna uma representação da cor seguindo o schema definido em
        CorViewSchema.
    """
    return {
        "id": cor.id,
        "nome": cor.nome,
        "hex": cor.hex
    }
