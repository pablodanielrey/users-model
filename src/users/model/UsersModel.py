import os
import uuid
import datetime
import base64
import logging
import json

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload, contains_eager, defer

from .entities.User import User, Mail, Phone, IdentityNumber, UserDegree, File, UsersLog, UserLogTypes

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
            User.id.op('~*')(query), \
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
    def get_person_identityNumber(cls, session, uid,iid):
        """
            Obtiene el documento solicitado
        """
        q = session.query(IdentityNumber).filter(IdentityNumber.user_id == uid, IdentityNumber.id == iid, IdentityNumber.deleted == None)
        i = q.one_or_none()
        if not i:
            return None
        return i

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
    def delete_person_degree(cls, session, uid, did, authorizer_id):
        """
            Elimina el titulo de la persona
        """
        d = session.query(UserDegree).filter(UserDegree.deleted == None, UserDegree.id == did, UserDegree.user_id == uid).first()
        if d:
            if d.file_id:
                f = session.query(File).filter(File.deleted == None, File.id == d.file_id).first()
                if f:
                    f.deleted = datetime.datetime.utcnow()
                    session.add(f)
                    fileToLog = {   'id': f.id,
                                    'created': f.created,
                                    'updated': f.updated,
                                    'deleted': f.deleted,
                                    'mimetype': f.mimetype,
                                    'content': f.content
                                }
                    fileDeleteLog = UsersLog()
                    fileDeleteLog.entity_id = f.id
                    fileDeleteLog.authorizer_id = authorizer_id
                    fileDeleteLog.type = UserLogTypes.DELETE
                    fileDeleteLog.data = json.dumps([fileToLog], default=str)
                    session.add(fileDeleteLog)
            d.deleted = datetime.datetime.utcnow()
            session.add(d)
            degreeToLog = { 'id': d.id,
                            'created': d.created,
                            'updated': d.updated,
                            'deleted': d.deleted,
                            'type' : d.type,
                            'title' : d.title,
                            'start' : d.start,
                            'user_id' : d.user_id,
                            'file_id' : d.file_id,
                        }
            degreeDeleteLog = UsersLog()
            degreeDeleteLog.entity_id = did
            degreeDeleteLog.authorizer_id = authorizer_id
            degreeDeleteLog.type = UserLogTypes.DELETE
            degreeDeleteLog.data = json.dumps([degreeToLog],default=str)
            session.add(degreeDeleteLog)
            return did
        return None

    @classmethod
    def delete_person_idnumber(cls, session, uid, pidnumberid, authorizer_id):
        """
            Elimina un documento de la persona
        """
        idnumber = session.query(IdentityNumber).filter(IdentityNumber.deleted == None, IdentityNumber.id == pidnumberid, IdentityNumber.user_id == uid).first()
        if idnumber:
            if idnumber.file_id:
                f = session.query(File).filter(File.deleted == None, File.id == d.file_id).first()
                if f:
                    f.deleted = datetime.datetime.utcnow()
                    session.add(f)
                    fileToLog = {   'id': f.id,
                                    'created': f.created,
                                    'updated': f.updated,
                                    'deleted': f.deleted,
                                    'mimetype': f.mimetype,
                                    'content': f.content
                                }
                    fileDeleteLog = UsersLog()
                    fileDeleteLog.entity_id = f.id
                    fileDeleteLog.authorizer_id = authorizer_id
                    fileDeleteLog.type = UserLogTypes.DELETE
                    fileDeleteLog.data = json.dumps([fileToLog], default=str)
                    session.add(fileDeleteLog)
            idnumber.deleted = datetime.datetime.utcnow()
            session.add(idnumber)
            idnumberToLog = { 'id': idnumber.id,
                            'created': idnumber.created,
                            'updated': idnumber.updated,
                            'deleted': idnumber.deleted,
                            'type' : idnumber.type,
                            'number' : idnumber.number,
                            'user_id' : idnumber.user_id,
                            'file_id' : idnumber.file_id,
                        }
            newLog = UsersLog()
            newLog.entity_id = pidnumberid
            newLog.authorizer_id = authorizer_id
            newLog.type = UserLogTypes.DELETE
            newLog.data = json.dumps([idnumberToLog],default=str)
            session.add(newLog)
            return idnumber.id
        return None
    
    @classmethod
    def delete_person_mail(cls, session, uid, pmid, authorizer_id):
        """
            Elimina un mail de la persona
        """
        pm = session.query(Mail).filter(Mail.deleted == None, Mail.id == pmid, Mail.user_id == uid).first()
        if pm:
            pm.deleted = datetime.datetime.utcnow()
            session.add(pm)
            mailDeleteLog ={ 'id': pm.id,
                          'created': pm.created,
                          'updated': pm.updated,
                          'deleted': pm.deleted,
                          'type': pm.type.value,
                          'email': pm.email,
                          'confirmed': pm.confirmed,
                          'user_id': pm.user_id,
            }
            newLog = UsersLog()
            newLog.entity_id = pmid
            newLog.authorizer_id = authorizer_id
            newLog.type = UserLogTypes.DELETE
            newLog.data = json.dumps([mailDeleteLog],default=str)
            session.add(newLog)
            return pm.id
        return None
    
    @classmethod
    def delete_person_phone(cls, session, uid, phid, authorizer_id):
        """
            Elimina un teléfono de la persona
        """
        ph = session.query(Phone).filter(Phone.deleted == None, Phone.id == phid, Phone.user_id == uid).first()
        if ph:
            ph.deleted = datetime.datetime.utcnow()
            session.add(ph)
            phoneDeleteLog ={ 'id': ph.id,
                          'created': ph.created,
                          'updated': ph.updated,
                          'deleted': ph.deleted,
                          'type': ph.type.value,
                          'number': ph.number,
                          'user_id': ph.user_id,
            }
            newLog = UsersLog()
            newLog.entity_id = phid
            newLog.authorizer_id = authorizer_id
            newLog.type = UserLogTypes.DELETE
            newLog.data = json.dumps([phoneDeleteLog],default=str)
            session.add(newLog)
            return ph.id
        return None
 
    @classmethod
    def get_file(cls, session, fid):
        return session.query(File).filter(File.id == fid).options(defer('content')).one_or_none()       