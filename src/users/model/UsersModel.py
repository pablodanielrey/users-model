import os
import uuid
import datetime
import base64
import logging
import json

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload, contains_eager

from .entities.User import User, Mail, Phone, IdentityNumber

class UsersModel:

    @classmethod
    def get_users(cls, session, uids=[]):
        """
        Obtiene los usuarios correspondientes a los uids proporcionados
        """
        users = []
        for uid in uids:
            q = session.query(User).filter(User.id == uid)
            q = q.options(joinedload('mails'), joinedload('phones'), joinedload('identity_numbers'))
            u = q.one()
            users.append(u)
        return users

    @classmethod
    def uuids(cls, session):
        q = session.query(User.id).distinct()
        Users = [u[0] for u in q]
        return Users

    @classmethod
    def search_user(cls, session, query):
        """
            retorna los uids que corresponden con la consulta de query
        """
        if not query:
            return []
        q = session.query(User.id).join(IdentityNumber)
        q = q.filter(or_(\
            User.firstname.op('~*')(query),\
            User.lastname.op('~*')(query),\
            IdentityNumber.number.op('~*')(query)\
        ))
        return q.all()

    @classmethod
    def get_uid_person_number(cls, session, person_number):
        """
            Obtiene el uid para ese documento
        """
        q = session.query(User.id).join(IdentityNumber).filter(IdentityNumber.number == person_number, User.deleted == None, IdentityNumber.deleted == None)
        u = q.one_or_none()
        if not u:
            return None
        return u.id