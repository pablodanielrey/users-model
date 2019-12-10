import pytz
from datetime import datetime, time, timedelta
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func, or_, ForeignKey
from sqlalchemy.orm import relationship

from . import Base

class LogUsuario(Base):

    __tablename__ = 'log_usuario'

    id = Column(String, primary_key=True, default=generateId)
    creado = Column(DateTime())
    actualizado = Column(DateTime())

    usuario_id = Column(String, ForeignKey('usuarios.id'))
    autorizador_id = Column(String, ForeignKey('usuarios.id'))
    datos = Column(String)


class Mail(Base):

    __tablename__ = 'mails'

    id = Column(String, primary_key=True, default=generateId)
    creado = Column(DateTime())
    actualizado = Column(DateTime())

    email = Column(String)
    confirmado = Column(DateTime)
    hash = Column(String)
    eliminado = Column(DateTime)

    usuario_id = Column(String, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario', back_populates='mails')


class Telefono(Base):

    __tablename__ = 'telefonos'

    id = Column(String, primary_key=True, default=generateId)
    creado = Column(DateTime())
    actualizado = Column(DateTime())

    numero = Column(String)
    tipo = Column(String)
    actualizado = Column(DateTime)
    eliminado = Column(DateTime)

    usuario_id = Column(String, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario', back_populates='telefonos')


class Usuario(Base):

    __tablename__ = 'usuarios'
    
    id = Column(String, primary_key=True, default=generateId)
    creado = Column(DateTime())
    actualizado = Column(DateTime())

    dni = Column(String, unique=True, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    genero = Column(String)
    nacimiento = Column(Date)
    ciudad = Column(String)
    pais = Column(String)
    direccion = Column(String)
    tipo = Column(String)

    avatar = Column(String)
    legajo = Column(String, unique=True)

    eliminado = Column(DateTime)

    mails = relationship('Mail', back_populates='usuario')
    telefonos = relationship('Telefono', back_populates='usuario')
    
    def obtener_nacimiento(self, tz):
        return self._localizar_fecha_en_zona(self.nacimiento, tz)

    def _localizar_fecha_en_zona(self, fecha, tz='America/Argentina/Buenos_Aires'):
        if fecha is None:
            return None
        timezone = pytz.timezone(tz)
        dt = datetime.combine(fecha, time(0))
        dt = timezone.localize(dt)
        return dt

