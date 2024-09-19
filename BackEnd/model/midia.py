from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario

class Midia(Base):
    __tablename__ = 'midia'

    id = Column("pk_midia", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    tipo = Column(String(30))
    stream = Column(String(40))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a mídia e o comentário.
    # Essa relação é implicita, não está salva na tabela 'midia',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome:str, tipo:str, stream:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Mídia

        Arguments:
            nome: nome da midia.
            tipo: tipo da mídia (Filme, série, documentário,...)
            stream: qual stream que passa a mídia
            data_insercao: data de quando a midia foi inserida à base
        """
        self.nome = nome
        self.tipo = tipo
        self.stream = stream

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Produto
        """
        self.comentarios.append(comentario)

