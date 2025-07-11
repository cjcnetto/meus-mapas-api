from datetime import datetime
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified

import os

# importando os elementos definidos no modelo
from models.base import Base
from models.point_of_interest import PointOfInterest
from models.map import Map

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
    os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)


@event.listens_for(Map, "before_update")
def receive_before_update_map(mapper, connection, target: Map):
    target.update_date = datetime.now()


@event.listens_for(PointOfInterest, "before_update")
def receive_before_update_poi(mapper, connection, target: PointOfInterest):
    target.update_date = datetime.now()
    flag_modified(target, "update_date")
