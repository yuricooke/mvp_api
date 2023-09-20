from pydantic import BaseModel
from typing import Optional, List
from model.paleta import Paleta



class PaletaSchema(BaseModel):
    """ Define como uma nova cor a ser inserida deve ser representada
    """
    nome: str = "Minha Paleta"
    neutral: str = "#FFFFFF"
    primary: str = "#FF0000"
    accent: str = "#F0F0F0"



class PaletaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da cor.
    """
    nome: str = "Minha Paleta"
    id: int = 1
    

class ListagemPaletasSchema(BaseModel):
    """ Define como uma listagem de cores será retornada.
    """
    paletas:List[PaletaSchema]


def apresenta_paletas(paletas: List[Paleta]):
    """ Retorna uma representação da paleta seguindo o schema definido em
        PaletaViewSchema.
    """
    result = []
    for paleta in paletas:
        result.append({
            "nome": paleta.nome,
            "neutral": paleta.neutral,
            "primary": paleta.primary,
            "accent": paleta.accent

        })

    return {"paletas": result}


class PaletaViewSchema(BaseModel):
    """ Define como uma cor será retornada: nome + neutral + primary + accent.
    """
    id: int = 1
    nome: str = "Minha Paleta"
    neutral: str = "#FFFFFF"
    primary: str = "#FF0000"
    accent: str = "#F0F0F0"


class PaletaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_paleta(paleta: Paleta):
    """ Retorna uma representação da paleta seguindo o schema definido em
        PaletaViewSchema.
    """
    return {
        "id": paleta.id,
        "nome": paleta.nome,
        "neutral": paleta.neutral,
        "primary": paleta.primary,
        "accent": paleta.accent
    }
