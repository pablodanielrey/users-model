import os
import uuid
import datetime
import base64
import logging
import json

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload, contains_eager

from .entities.User import User, Mail, Phone

class UsersModel:

    @classmethod
    def get_users(cls, session, uids=[]):
        users = []
        for uid in uids:
            q = session.query(User).filter(User.id == uid)
            q = q.options(joinedload('mails'), joinedload('phones'))
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
        q = session.query(User.id)
        q = q.filter(or_(\
            User.person_number.op('~*')(query),\
            User.firstname.op('~*')(query),\
            User.lastname.op('~*')(query)\
        ))
        return q.all()

