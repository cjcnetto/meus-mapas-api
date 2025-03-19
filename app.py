from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from schemas import *
from flask_cors import CORS
from services import mapService, pointOfInterestService

info = Info(title="My Maps API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
map_tag = Tag(name="Map", description="Endpoints to Create Update and Delete a Map, a Map represents a collection of points")
point_of_interest_tag = Tag(name="Point of Interest", description="CRUD of points of interest")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.get('/maps', tags=[map_tag],
         responses={"200": ListMapResponse, "404": ErrorSchema})
def get_maps():
    """Returns all maps in the database"""
    try:
        maps = mapService.list_all()
        return maps.to_json(), 200
    except Exception as e:
        return ErrorSchema(message=str(e)).to_json(), 404

@app.post('/map', tags=[map_tag],
          responses={"200": UpsertResponse, "409": ErrorSchema, "400": ErrorSchema})
def add_map(form: UpsertRequest):
    """Adds or update a map to the database by its id, if the id is not present a new map is created"""
    try:
        response = mapService.upsert(form)
        if(response.map == None):
            return ErrorSchema(message=response.message).to_json(), 400
        return response.to_json(), 200
    except Exception as e:
        return ErrorSchema(message=str(e)).to_json(), 409

@app.get('/map', tags=[map_tag],
         responses={"200": MapSchema, "404": ErrorSchema})
def get_map(query: FindMapRequest):
    """Get a map by its id"""
    try:
        map = mapService.get(query)
        return map.to_json(), 200
    except Exception as e:
        return ErrorSchema(message=str(e)).to_json(), 404

@app.delete('/map', tags=[map_tag],
            responses={"200": DelSchema, "404": ErrorSchema})
def del_map(query: FindMapRequest):
    """Delete a map by its id"""
    try:
        map = mapService.delete(query)
        return map.to_json(), 200
    except Exception as e:
        return ErrorSchema(message=str(e)).to_json(), 404
    
@app.get('/points', tags=[point_of_interest_tag],
         responses={"200": ListPointOfInterestResponse, "404": ErrorSchema})
def get_points(query: FindMapRequest):
    """Returns all points of interest in a map"""
    try:
        points = pointOfInterestService.list_all(query)
        return points.to_json(), 200
    except Exception as e:
        return ErrorSchema(message=str(e)).to_json(), 404

@app.post('/point', tags=[point_of_interest_tag],
          responses={"200": UpsertPointOfInterestResponse, "409": ErrorSchema, "400": ErrorSchema})
def add_point(form: UpsertPointOfInterestRequest):
    """Adds or update a point to the database by its id, if the id is not present a new map is created"""
    try:
        response = pointOfInterestService.upsert(form)
        if(response.point_of_interest == None):
            return ErrorSchema(message=response.message).to_json(), 400
        return response.to_json(), 200
    except Exception as e:
        return ErrorSchema(message=str(e)).to_json(), 409

@app.delete('/point', tags=[point_of_interest_tag],
            responses={"200": DelSchema, "404": ErrorSchema})
def del_point(query: FindPointOfInterestRequest):
    """Delete a point by the map and point id"""
    try:
        point = pointOfInterestService.delete(query)
        return point.to_json(), 200
    except Exception as e:
        return ErrorSchema(message=str(e)).to_json(), 404
