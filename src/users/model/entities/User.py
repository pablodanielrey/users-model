import pytz
import uuid
from datetime import datetime, time, timedelta
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func, or_, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from enum import Enum

from . import Base


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
    

class PhoneTypes(Enum):
    CELLPHONE = 'CELLPHONE'
    LANDLINE = 'LANDLINE'


class Phone(Base):

    __tablename__ = 'phones'
    
    number = Column(String)
    type = Column(SQLEnum(PhoneTypes))

    user_id = Column(String, ForeignKey('users.id'))


class User(Base):

    __tablename__ = 'users'
    
    lastname = Column(String)
    firstname = Column(String)
    gender = Column(String)
    marital_status = Column(String)
    birthplace = Column(String)
    birthdate = Column(DateTime())
    residence = Column(String)
    address = Column(String)
        
    mails = relationship('Mail')
    phones = relationship('Phone')
    identity_numbers = relationship('IdentityNumber')

    """
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
    """


class IdentityNumberTypes(Enum):
    DNI = 'DNI'
    LC = 'LC'
    LE = 'LE'
    PASSPORT = 'PASSPORT'
    CUIL = 'CUIL'
    CUIT = 'CUIT'


class IdentityNumber(Base):

    __tablename__ = 'identity_numbers'

    type = Column(SQLEnum(IdentityNumberTypes))
    number = Column(String)

    user_id = Column(String, ForeignKey('users.id'))

    file_id = Column(String, ForeignKey('files.id'))
    file = relationship('File')


class DegreeTypes(Enum):
    ELEMENTARY = 'ELEMENTARY'
    HIGHER = 'HIGHER'
    COLLEGE = 'COLLEGE'
    MASTER = 'MASTER'
    DOCTORAL = 'DOCTORAL'


class UserDegree(Base):

    __tablename__ = 'degree'

    type = Column(SQLEnum(DegreeTypes))
    title = Column(String)
    start = Column(DateTime)

    user_id = Column(String, ForeignKey('users.id'))

    file_id = Column(String, ForeignKey('files.id'))
    file = relationship('File')


class File(Base):

    __tablename__ = 'files'

    mimetype = Column(String)
    content = Column(String)
   