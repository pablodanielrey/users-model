import pytz
import uuid
from datetime import datetime, time, timedelta
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func, or_, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from enum import Enum

from . import Base


def generateId():
    return str(uuid.uuid4())

class UsersLog(Base):

    __tablename__ = 'users_log'

    id = Column(String, primary_key=True, default=generateId())
    created = Column(DateTime())
    updated = Column(DateTime())

    user_id = Column(String, ForeignKey('users.id'))
    authorizer_id = Column(String, ForeignKey('users.id'))
    data = Column(String)

    def __init__(self):
        self.id = generateId()


class MailTypes(Enum):
    NOTIFICATION = 'NOTIFICATION'
    INSTITUTIONAL = 'INSTITUTIONAL'
    ALTERNATIVE = 'ALTERNATIVE'

class Mail(Base):

    __tablename__ = 'mails'

    id = Column(String, primary_key=True, default=generateId())
    created = Column(DateTime())
    updated = Column(DateTime())
    deleted = Column(DateTime())

    type = Column(SQLEnum(MailTypes))

    email = Column(String)
    confirmed = Column(DateTime()) 

    user_id = Column(String, ForeignKey('users.id'))
    user = relationship('User')

    def __init__(self):
        self.id = generateId()

class PhoneTypes(Enum):
    CELLPHONE = 'CELLPHONE'
    LANDLINE = 'LANDLINE'

class Phone(Base):

    __tablename__ = 'phones'

    id = Column(String, primary_key=True, default=generateId())
    created = Column(DateTime())
    updated = Column(DateTime())
    deleted = Column(DateTime())
    
    number = Column(String)
    type = Column(SQLEnum(MailTypes))

    user_id = Column(String, ForeignKey('users.id'))
    user = relationship('User')

    def __init__(self):
        self.id = generateId()


class User(Base):

    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, default=generateId())
    created = Column(DateTime())
    updated = Column(DateTime())
    deleted = Column(DateTime())

    lastname = Column(String)
    firstname = Column(String)
    person_number_type = Column(String)
    person_number = Column(String, unique=True, nullable=False)
    gender = Column(String)
    marital_status = Column(String)
    birthplace = Column(String)
    birthdate = Column(DateTime())
    residence = Column(String)
    address = Column(String)
        
    mails = relationship('Mail', back_populates='user')
    phones = relationship('Phone', back_populates='user')
    
    def __init__(self):
        self.id = generateId()

    def get_birthdate(self, tz):
        return self._localize_date_on_zone(self.birthdate, tz)

    def _localize_date_on_zone(self, date, tz='America/Argentina/Buenos_Aires'):
        if date is None:
            return None
        timezone = pytz.timezone(tz)
        dt = datetime.combine(date, time(0))
        dt = timezone.localize(dt)
        return dt


class UserFiles(Base):

    __tablename__ = 'user_files'
    
    id = Column(String, primary_key=True, default=generateId())
    created = Column(DateTime())
    updated = Column(DateTime())
    deleted = Column(DateTime())

    mimetype = Column(String)
    type = Column(String)
    content = Column(String)

    def __init__(self):
        self.id = generateId()