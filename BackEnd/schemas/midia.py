from pydantic import BaseModel
from typing import Optional, List
from model.midia import Midia

from schemas import ComentarioSchema


class MidiaSchema(BaseModel):
    """Define como uma nova mídia a ser inserida deve ser representada
    """
    nome: str = "Top Gun"
    tipo: str = "Filme"
    stream: str = "Netflix"


class MidiaBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da midia.
    """
    nome: str = "Teste"


class ListagemMidiasSchema(BaseModel):
    """Define como uma listagem de mídias será retornada.
    """
    midias:List[MidiaSchema]


def apresenta_midias(midias: List[Midia]):
    """ Retorna uma representação da mídia seguindo o schema definido em
        MidiaViewSchema.
    """
    result = []
    for midia in midias:
        result.append({
            "nome": midia.nome,
            "tipo": midia.tipo,
            "stream": midia.stream,
        })

    return {"midias": result}


class MidiaViewSchema(BaseModel):
    """Define como uma mídia será retornada: mídia + comentários.
    """
    id: int = 1
    nome: str = "Top Gun"
    tipo: str = "Filme"
    stream: str = "Netflix"
    total_comentarios: int = 1
    comentarios: List[ComentarioSchema]


class MidiaDelSchema(BaseModel):
    """Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
    nome: str

def apresenta_midia(midia: Midia):
    """Retorna uma representação da mídia seguindo o schema definido em
    MidiaViewSchema
    """
    return{
        "id": midia.id,
        "nome": midia.nome,
        "tipo": midia.tipo,
        "stream": midia.stream,
        "total_comentarios": len(midia.comentarios),
        "comentarios": [{"texto": c.texto} for c in midia.comentarios]
    }


class TipoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no tipo da midia.
    """
    tipo: str = "Filme, Série, Novela, Documentário ou Outros"


class StreamBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no stream da midia.
    """
    stream: str = "Netflix, Prime Vídeo, Disney+, GloboPlay, Apple TV, Paramount + ou Outros"