import os
import uuid
import datetime
import base64
import logging
import json

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload, contains_eager

from .MailsModel import MailsModel
from .entities.Usuario import Usuario, Mail, Telefono, LogUsuario

class UsersModel:

    @classmethod
    def get_users(cls, session, uids=[]):
        users = []
        for uid in uids:
            q = session.query(Usuario).filter(Usuario.id == uid)
            q = q.options(joinedload('mails'), joinedload('telefonos'))
            u = q.one()
            users.append(u)
        return users

    @classmethod
    def usuarios_uuids(cls, session):
        q = session.query(Usuario.id).distinct()
        usuarios = [u[0] for u in q]
        return usuarios

    @classmethod
    def search_user(cls, session, query):
        """
            retorna los uids que corresponden con la consulta de query
        """
        if not query:
            return []
        q = session.query(Usuario.id)
        q = q.filter(or_(\
            Usuario.dni.op('~*')(query),\
            Usuario.nombre.op('~*')(query),\
            Usuario.apellido.op('~*')(query)\
        ))
        return q.all()

