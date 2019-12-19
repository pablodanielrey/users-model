import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

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

class MyBaseClass:

    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    deleted = Column(DateTime)

    def __init__(self):
        self.id = generateId()

#Base = declarative_base(cls=(JsonSerializableBase,MyBaseClass))
Base = declarative_base(cls=MyBaseClass)