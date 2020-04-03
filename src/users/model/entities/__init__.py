import os
import uuid

"""
'''
    problema de codificación a json en flask.
    respuesta :
    https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
'''
from sqlalchemy.ext.declarative import DeclarativeMeta
import json as json
import datetime

class BasicEncoder(json.JSONEncoder):

    @staticmethod
    def encode_c(o):
        if isinstance(o, datetime.datetime):
            return o.isoformat(' ')
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, set):
            return list(o)
        if isinstance(o, str):
            return o
        return json.dumps(o)

    #pylint: disable=all
    def default(self, o):
        return self.encode_c(o)


class AlchemyEncoder(json.JSONEncoder):
    #pylint: disable=all
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            data = {}
            fields = o.__serialize__ if hasattr(o, '__serialize__') else dir(o)
            for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
                value = o.__getattribute__(field)
                try:
                    value = BasicEncoder.encode_c(value)
                    data[field] = value
                except TypeError:
                    data[field] = None
            return data
        return super(AlchemyEncoder,self).default(o)
"""

from sqlalchemy import create_engine, func, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin

def generateId():
    return str(uuid.uuid4())

class MyBaseClass(SerializerMixin):

    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    deleted = Column(DateTime)

Base = declarative_base(cls=MyBaseClass)