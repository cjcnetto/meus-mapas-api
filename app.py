from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from exceptions.not_found_exception import NotFoundException
from exceptions.validation_exception import ValidationException
from schemas import (
    ListMapResponse,
    ErrorSchema,
    UpsertMapRequest,
    UpsertMapResponse,
    DelSchema,
    FindMapRequest,
    ListPointOfInterestResponse,
    UpsertPointOfInterestRequest,
    UpsertPointOfInterestResponse,
    FindPointOfInterestRequest
)
from flask_cors import CORS
from services import map_service

info = Info(title="Meus Mapas API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Documentação em swagger")
map_tag = Tag(name="Map",
              description="Conjunto de operações para a CRUD de mapas")
point_of_interest_tag = Tag(name="Point of Interest",
                            description=(
                                "Conjunto de operações para a CRUD dos "
                                "pontos de interesse de um mapa"
                            ))


@app.get('/', tags=[home_tag])
def home():
    """
    Redireciona para /openapi, tela que permite a escolha do estilo de
    documentação.
    """
    return redirect('/openapi/swagger')


@app.get('/maps', tags=[map_tag],
         responses={"200": ListMapResponse, "404": ErrorSchema})
def get_maps():
    """Retorna todos os mapas cadastrados na base de dados"""
    try:
        maps = map_service.list_all_maps()
        return maps.to_json(), 200
    except Exception as e:
        return __treat_error(e)


@app.post(
    '/map',
    tags=[map_tag],
    responses={
        "200": UpsertMapResponse,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def add_map(form: UpsertMapRequest):
    """
    Insere um novo mapa ou atualiza um existente. Se o id for definido como -1
    ou não for passado, um novo mapa é criado.
    """
    try:
        response = map_service.upsert_map(form)
        if (response.map is None):
            return ErrorSchema(message=response.message).to_json(), 400
        return response.to_json(), 200
    except Exception as e:
        return __treat_error(e)


@app.delete('/map', tags=[map_tag],
            responses={"200": DelSchema, "404": ErrorSchema})
def del_map(query: FindMapRequest):
    """Remove um mapa da base de dados"""
    try:
        map = map_service.delete(query)
        return map.to_json(), 200
    except Exception as e:
        return __treat_error(e)


@app.get('/points', tags=[point_of_interest_tag],
         responses={"200": ListPointOfInterestResponse, "404": ErrorSchema})
def get_points(query: FindMapRequest):
    """Retorna todos os pontos de interesse de um mapa especifico"""
    try:
        points = map_service.list_all_points(query)
        return points.to_json(), 200
    except Exception as e:
        return __treat_error(e)


@app.post(
    '/point',
    tags=[point_of_interest_tag],
    responses={
        "200": UpsertPointOfInterestResponse,
        "409": ErrorSchema,
        "400": ErrorSchema
    }
)
def add_point(form: UpsertPointOfInterestRequest):
    """
    Insere um novo ponto de interesse ou atualiza um existente,
    dentro de um mapa.
    Se o id for definido como -1 ou não for passado,
    um novo ponto de interesse é criado.
    """
    try:
        response = map_service.upsert_point(form)
        if (response.point_of_interest is None):
            return ErrorSchema(message=response.message).to_json(), 400
        return response.to_json(), 200
    except Exception as e:
        return __treat_error(e)


@app.delete('/point', tags=[point_of_interest_tag],
            responses={"200": DelSchema, "404": ErrorSchema})
def del_point(query: FindPointOfInterestRequest):
    """Delete a point by the map and point id"""
    try:
        point = map_service.delete_point(query)
        return point.to_json(), 200
    except Exception as e:
        return __treat_error(e)


def __treat_error(e):
    """Tratamento de erro padrão para o flask-openapi3"""
    message = str(e)
    error = ErrorSchema(message=message).to_json()
    if (isinstance(e, NotFoundException)):
        return error, 404
    if (isinstance(e, ValidationException)):
        return error, 409
    return error, 500
