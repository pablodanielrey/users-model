import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .User import User, Phone, Mail, UserFiles, MailTypes, PhoneTypes, UserFileTypes

def crear_tablas():
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['USERS_DB_USER'],
        os.environ['USERS_DB_PASSWORD'],
        os.environ['USERS_DB_HOST'],
        os.environ.get('USERS_DB_PORT',5432),
        os.environ['USERS_DB_NAME']
    ), echo=True)
    Base.metadata.create_all(engine)

