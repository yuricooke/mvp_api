from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Cor
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="603010 Generator", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cor_tag = Tag(name="Cor", description="Adição, visualização e remoção de cores à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


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

