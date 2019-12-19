import pytz
import uuid
from datetime import datetime, time, timedelta
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func, or_, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from enum import Enum

from . import Base


def generateId():
    return str(uuid.uuid4())

class UserLogTypes(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'

class UsersLog(Base):

    __tablename__ = 'users_log'

    type = Column(SQLEnum(UserLogTypes))
    entity_id = Column(String)
    authorizer_id = Column(String)
    data = Column(String)


class MailTypes(Enum):
    NOTIFICATION = 'NOTIFICATION'
    INSTITUTIONAL = 'INSTITUTIONAL'
    ALTERNATIVE = 'ALTERNATIVE'

class Mail(Base):

    __tablename__ = 'mails'

    type = Column(SQLEnum(MailTypes))

    email = Column(String)
    confirmed = Column(DateTime()) 

    user_id = Column(String, ForeignKey('users.id'))
    user = relationship('User')


class PhoneTypes(Enum):
    CELLPHONE = 'CELLPHONE'
    LANDLINE = 'LANDLINE'

class Phone(Base):

    __tablename__ = 'phones'
    
    number = Column(String)
    type = Column(SQLEnum(PhoneTypes))

    user_id = Column(String, ForeignKey('users.id'))
    user = relationship('User')


class User(Base):

    __tablename__ = 'users'
    
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
    

    def get_birthdate(self, tz):
        return self._localize_date_on_zone(self.birthdate, tz)

    def _localize_date_on_zone(self, date, tz='America/Argentina/Buenos_Aires'):
        if date is None:
            return None
        timezone = pytz.timezone(tz)
        dt = datetime.combine(date, time(0))
        dt = timezone.localize(dt)
        return dt

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UserFileTypes(Enum):
    PERSONNUMBER = 'PERSONNUMBER'
    LABORALNUMBER = 'LABORALNUMBER'

class UserFiles(Base):

    __tablename__ = 'user_files'

    mimetype = Column(String)
    type = Column(SQLEnum(UserFileTypes))
    content = Column(String)

    