from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Midia, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title = "Meu API", version = "1.0.0")
app = OpenAPI(__name__, info = info)
CORS(app)

# Definindo tags
home_tag = Tag(name = "Documentação", description = "Seleção de documentação: Swagger.")
midia_tag = Tag(name = "Mídia", description = "Adição, visualização e remoção de mídias à base.")
comentario_tag = Tag(name = "Comentário", description = "Adição de um comentário à uma mídia cadastrada na base")

@app.get('/', tags = [home_tag])
def home():
    """Redireciona para /openapi/swagger, indo diretamente para o estilo de 
    documentação Swagger
    """
    return redirect('/openapi/swagger')

@app.post('/midia', tags = [midia_tag], 
          responses = {"200": MidiaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_midia(form: MidiaSchema):
    """Adiciona uma nova mídia à base de dados
    Retorna uma representação das mídias e comentários associados.
    """
    midia = Midia(
        nome = form.nome,
        tipo = form.tipo,
        stream = form.stream)
    logger.debug(f"Adicionando mídia de nome: '{midia.nome}'")
    try: 
        # Criando conexão com a base
        session = Session()
        # Adicionando mídia
        session.add(midia)
        # Efetivando o comando de adição de nova mídia na tabela
        session.commit()
        logger.debug(f"Adicionando mídia de nome: '{midia.nome}'")
        return apresenta_midia(midia), 200
    
    except IntegrityError as e:
        # Como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Mídia de mesmo nome já salvo na base."
        logger.warning(f"Erro ao adicionar mídia '{midia.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    
    except Exception as e:
        # Caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova mídia."
        logger.warning(f"Erro ao adicionar mídia '{midia.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    

@app.get('/midias', tags = [midia_tag],
         responses = {"200": ListagemMidiasSchema, "400": ErrorSchema})
def get_midias():
    """Faz a busca por todas as mídias cadastradas.
    Retorna uma representação da listagem de mídias.
    """
    logger.debug(f"Coletando mídias ")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    midias = session.query(Midia).all()

    if not midias:
        # Se não há mídias cadastradas
        return {"mídias":[]}, 200
    else:
        logger.debug(f"%d mídias encontradas" % len(midias))
        # Retorna a representação das mídias
        print(midias)
        return apresenta_midias(midias), 200
    

@app.get('/midia', tags = [midia_tag],
         responses = {"200": MidiaBuscaSchema, "400": ErrorSchema})
def get_midia(query: MidiaBuscaSchema):
    """Faz a busca por uma mídia a partir do id da mídia.
    Retorna uma representação das mídias e comentários associados.
    """
    midia_id = query.nome
    logger.debug(f"Coletando dados sobre mídia #{midia_id}")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    midia = session.query(Midia).filter(Midia.id == midia_id).first()

    if not midia:
        # Se a mídia não foi encontrada
        error_msg = "Mídia não encontrada na base"
        logger.warning(f"Erro ao buscar mídia '{midia_id}', {error_msg}")
        return {"mesage": error_msg}, 400
    else:
        logger.debug(f"Mídia encontrada: '{midia.nome}'")
        # Retorna a representação da mídia
        return apresenta_midia(midia), 200
    

@app.delete('/midia', tags = [midia_tag],
            responses = {"200": MidiaDelSchema, "400": ErrorSchema})
def del_midia(query: MidiaBuscaSchema):
    """Deleta uma mídia a partir do nome da mídia informada
    Retorna uma mensagem de confirmação da remoção
    """
    midia_nome = unquote(unquote(query.nome))
    print(midia_nome)
    logger.debug(f"Deletando dados sobre a mídia #{midia_nome}")
    # Criando conexão com a base
    session = Session()
    # Fazendo a remoção
    count = session.query(Midia).filter(Midia.nome == midia_nome).delete()
    session.commit()

    if count:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando mídia #{midia_nome}")
        return {"mesage": "Mídia removida", "id": midia_nome}
    else:
        # Se a mídia não foi encontrada
        error_msg = "Mídia não encontrada na base"
        logger.warning(f"Erro ao deletar mídia #'{midia_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    

@app.post('/comentario', tags = [comentario_tag],
          responses = {"200": MidiaViewSchema, "404": ErrorSchema})
def add_comentario(form:ComentarioSchema):
    """Adiciona de um novo comentário à uma mídia cadastrada na base identificada pelo id.
    Retorna uma representação das mídias e comentários associados.
    """
    midia_id = form.midia_id
    logger.debug(f"Adicionando comentários à mídia #{midia_id}")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca pela mídia
    midia = session.query(Midia).filter(Midia.id == midia_id).first()

    if not midia:
        # Se mídia não encontrada
        error_msg = "Mídia não encontrada na base."
        logger.warning(f"Erro ao adicionar comentário à mídia '{midia_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    
    # Criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # Adicionando o comentário à mídia
    midia.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário à mídia #{midia_id}")

    # Retorna a representação da mídia
    return apresenta_midia(midia), 200


@app.get('/midiastipo', tags = [midia_tag],
         responses = {"200": ListagemMidiasSchema, "404": ErrorSchema})
def get_tipo(query: TipoBuscaSchema):
    """Faz a busca por todas as mídias cadastradas.
    Retorna uma representação da listagem de mídias por tipo.
    """

    midia_id = query.tipo
    logger.debug(f"Coletando dados sobre mídia #{midia_id}")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    midia = session.query(Midia).filter(Midia.tipo == midia_id).all()

    if not midia:
        # Se a mídia não foi encontrada
        error_msg = "Mídia não encontrada na base"
        logger.warning(f"Erro ao buscar mídia '{midia_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    
    else:
        logger.debug(f"%d mídias encontradas" % len(midia))
        # Retorna a representação da mídia
        print(midia)
        return apresenta_midias(midia), 200
    

@app.get('/midiasstream', tags = [midia_tag],
         responses = {"200": ListagemMidiasSchema, "404": ErrorSchema})
def get_stream(query: StreamBuscaSchema):
    """Faz a busca por todas as mídias cadastradas.
    Retorna uma representação da listagem de mídias por stream.
    """

    midia_id = query.stream
    logger.debug(f"Coletando dados sobre mídia #{midia_id}")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    midia = session.query(Midia).filter(Midia.stream == midia_id).all()

    if not midia:
        # Se a mídia não foi encontrada
        error_msg = "Mídia não encontrada na base."
        logger.warning(f"Erro ao buscar mídia '{midia_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    
    else:
        logger.debug(f"%d mídias encontradas" % len(midia))
        # Retorna a representação das mídias
        print(midia)
        return apresenta_midias(midia), 200