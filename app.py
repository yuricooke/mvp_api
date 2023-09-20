from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Cor, Paleta
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="603010 Generator", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cor_tag = Tag(name="Cor", description="Adição, visualização e remoção de cores à base")
paleta_tag = Tag(name="Paleta", description="Adição, visualização e remoção de paletas à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# METODOS PARA CORES

@app.post('/cor', tags=[cor_tag],
          responses={"200": CorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cor(form: CorSchema):
    """Adiciona uma nova cor à base de dados

    Retorna uma representação das cores e comentários associados.
    """
    cor = Cor(
        nome=form.nome,
        hex=form.hex)
    logger.debug(f"Adicionando cor de nome: '{cor.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando cor
        session.add(cor)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cor de nome: '{cor.nome}'")
        return apresenta_cor(cor), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cor de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar cor'{cor.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cor '{cor.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/cores', tags=[cor_tag],
         responses={"200": ListagemCoresSchema, "404": ErrorSchema})
def get_cores():
    """Faz a busca por todas as cores salvas

    Retorna uma representação da listagem de cores.
    """
    logger.debug(f"Coletando cores ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cores = session.query(Cor).all()

    if not cores:
        # se não há cores cadastradas
        return {"cores": []}, 200
    else:
        logger.debug(f"%d cores econtradas" % len(cores))
        # retorna a representação da cor
        print(cores)
        return apresenta_cores(cores), 200


@app.get('/cor', tags=[cor_tag],
         responses={"200": CorViewSchema, "404": ErrorSchema})
def get_cor(query: CorBuscaSchema):
    """Faz a busca por uma Cor a partir do id da cor

    Retorna uma representação das cores salvas.
    """
    cor_id = query.id
    logger.debug(f"Coletando dados sobre a cor #{cor_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cor = session.query(Cor).filter(Cor.id == cor_id).first()

    if not cor:
        # se a cor não foi encontrada
        error_msg = "Cor não encontrado na base :/"
        logger.warning(f"Erro ao buscar cor '{cor_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Cor econtrada: '{cor.nome}'")
        # retorna a representação de cor
        return apresenta_cor(cor), 200


@app.delete('/cor', tags=[cor_tag],
            responses={"200": CorDelSchema, "404": ErrorSchema})
def del_cor(query: CorBuscaSchema):
    """Deleta uma Cor a partir do nome da cor informada

    Retorna uma mensagem de confirmação da remoção.
    """
    cor_nome = unquote(unquote(query.nome))
    print(cor_nome)
    logger.debug(f"Deletando dados sobre a cor #{cor_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cor).filter(Cor.nome == cor_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada a cor #{cor_nome}")
        return {"mesage": "Cor removida", "nome": cor_nome}
    else:
        # se a cor não foi encontrada
        error_msg = "Cor não encontrada na base :/"
        logger.warning(f"Erro ao deletar a cor #'{cor_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


# METODOS PARA PALETAS -----


@app.post('/paleta', tags=[paleta_tag],
          responses={"200": PaletaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_paleta(form: PaletaSchema):
    """Adiciona uma nova paleta à base de dados

    Retorna uma representação das paletas e comentários associados.
    """
    paleta = Paleta(
        nome=form.nome,
        neutral=form.neutral,
        primary=form.primary,
        accent=form.accent)
    logger.debug(f"Adicionando paleta de nome: '{paleta.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando paleta
        session.add(paleta)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado paleta de nome: '{paleta.nome}'")
        return apresenta_paleta(paleta), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Paleta de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar paleta'{paleta.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paleta '{paleta.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/paletas', tags=[paleta_tag],
         responses={"200": ListagemPaletasSchema, "404": ErrorSchema})
def get_paletas():
    """Faz a busca por todas as cores salvas

    Retorna uma representação da listagem de cores.
    """
    logger.debug(f"Coletando paletas")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paletas = session.query(Paleta).all()

    if not paletas:
        # se não há cores cadastradas
        return {"cores": []}, 200
    else:
        logger.debug(f"%d cores econtradas" % len(paletas))
        # retorna a representação da cor
        print(paletas)
        return apresenta_paletas(paletas), 200


@app.get('/paleta', tags=[paleta_tag],
         responses={"200": PaletaViewSchema, "404": ErrorSchema})
def get_paleta(query: PaletaBuscaSchema):
    """Faz a busca por uma paleta a partir do id da paleta

    Retorna uma representação das paletaes salvas.
    """
    paleta_id = query.id
    logger.debug(f"Coletando dados sobre a paleta #{paleta_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paleta = session.query(Paleta.id).filter(Paleta.id == paleta_id).first()

    if not paleta:
        # se a cor não foi encontrada
        error_msg = "Paleta não encontrado na base :/"
        logger.warning(f"Erro ao buscar cor '{paleta_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Paleta econtrada: '{paleta.nome}'")
        # retorna a representação de paleta
        return apresenta_paleta(paleta), 200


@app.delete('/paleta', tags=[paleta_tag],
            responses={"200": CorDelSchema, "404": ErrorSchema})
def del_paleta(query: CorBuscaSchema):
    """Deleta uma paleta a partir do nome da paleta informada

    Retorna uma mensagem de confirmação da remoção.
    """
    paleta_nome = unquote(unquote(query.nome))
    print(paleta_nome)
    logger.debug(f"Deletando dados sobre a paleta #{paleta_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Paleta).filter(Paleta.nome == paleta_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada a paleta #{paleta_nome}")
        return {"mesage": "Paleta removida", "nome": paleta_nome}
    else:
        # se a cor não foi encontrada
        error_msg = "Paleta não encontrada na base :/"
        logger.warning(f"Erro ao deletar a paleta #'{paleta_nome}', {error_msg}")
        return {"mesage": error_msg}, 404