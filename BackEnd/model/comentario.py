from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model import Base


class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key = True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e uma mídia.
    # Aqui está sendo definido a coluna 'midia' que vai guardar
    # a referencia da midia, a chave estrangeira que relaciona 
    # uma mídia ao comentário.
    midia = Column(Integer, ForeignKey("midia.pk_midia"), nullable=False)

    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        """Cria um Comentário

        Arguments:
            texto: o texto de um comentário
            data_insercao: data de quando um comentário foi feito ou inserido 
            à Base
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
