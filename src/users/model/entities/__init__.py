import os
import uuid
from sqlalchemy import create_engine, func, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

def generateId():
    return str(uuid.uuid4())

class MyBaseClass:

    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    deleted = Column(DateTime)

Base = declarative_base(cls=MyBaseClass)