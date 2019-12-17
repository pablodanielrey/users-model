import pytz
import uuid
from datetime import datetime, time, timedelta
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func, or_, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


def generateId():
    return str(uuid.uuid4())

class UsersLog(Base):

    __tablename__ = 'users_log'

    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime())
    updated = Column(DateTime())

    user_id = Column(String, ForeignKey('users.id'))
    authorizer_id = Column(String, ForeignKey('users.id'))
    data = Column(String)


class Mail(Base):

    __tablename__ = 'mails'

    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime())
    updated = Column(DateTime())
    deleted = Column(DateTime())

    email = Column(String)
    confirmed = Column(DateTime())
    hash = Column(String)    

    user_id = Column(String, ForeignKey('users.id'))
    user = relationship('User', back_populates='mails')


class Phone(Base):

    __tablename__ = 'phones'

    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime())
    updated = Column(DateTime())
    deleted = Column(DateTime())
    
    number = Column(String)
    phone_type = Column(String)

    user_id = Column(String, ForeignKey('users.id'))
    user = relationship('User', back_populates='phones')


class User(Base):

    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, default=generateId)
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
        
    mails = relationship('Mail', back_populates='users')
    phones = relationship('Phone', back_populates='users')
    
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
    
    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime())
    updated = Column(DateTime())
    deleted = Column(DateTime())

    mimetype = Column(String)
    type = Column(String)
    content = Column(String)