import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .Usuario import Usuario, Telefono, Mail

def crear_tablas():
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASSWORD'],
        os.environ['DB_HOST'],
        os.environ.get('DB_PORT',5432),
        os.environ['DB_NAME']
    ), echo=True)
    Base.metadata.create_all(engine)

