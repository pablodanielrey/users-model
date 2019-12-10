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
    def get_user(cls, session, uid):
        assert uid is not None
        q = session.query(Usuario).filter(Usuario.id == uid)
        q = q.options(joinedload('mails'), joinedload('telefonos'))
        u = q.one()
        return u

    @classmethod
    def usuarios_uuids(cls, session):
        q = session.query(Usuario.id).distinct()
        usuarios = [u[0] for u in q]
        return usuarios
