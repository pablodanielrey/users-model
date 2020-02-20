import os
import uuid
import datetime
import base64
import logging
import json

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload, contains_eager, defer

from .entities.User import User, Mail, Phone, IdentityNumber, UserDegree, File

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

    @classmethod
    def get_uid_person_student(cls, session, student_number):
        """
            Obtiene el uid para el legajo
        """
        q = session.query(User.id).join(IdentityNumber).filter(IdentityNumber.number == student_number, User.deleted == None, IdentityNumber.deleted == None)
        u = q.one_or_none()
        if not u:
            return None
        return u.id

    @classmethod
    def get_person_degrees(cls, session, uid):
        """
            Obtiene los titulos para el usuario solicitado
        """
        q = session.query(UserDegree).filter(UserDegree.user_id == uid, UserDegree.deleted == None)
        d = q.all()
        if not d:
            return None
        return d

    @classmethod
    def get_person_degree(cls, session, uid,did):
        """
            Obtiene el titulo solicitado
        """
        q = session.query(UserDegree).filter(UserDegree.user_id == uid, UserDegree.id == did, UserDegree.deleted == None)
        d = q.one_or_none()
        if not d:
            return None
        return d

    @classmethod
    def delete_person_degree(cls, session, uid, tid):
        """
            Elimina el titulo de la persona
        """
        t = session.query(UserDegree).filter(UserDegree.deleted == None, UserDegree.id == tid, UserDegree.user_id == uid).first()
        if t:
            t.deleted = datetime.datetime.utcnow()
            session.add(t)
            return tid
        return None
 
    @classmethod
    def get_file(cls, session, fid):
        return session.query(File).filter(File.id == fid).options(defer('content')).one_or_none()       