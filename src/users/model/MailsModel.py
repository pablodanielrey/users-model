import os
import base64
import requests
from jinja2 import Environment, PackageLoader, FileSystemLoader

class MailsModel:

    EMAILS_API_URL = os.environ['EMAILS_API_URL']
    env = Environment(loader=PackageLoader('users.model.templates','.'))

    INTERNAL_DOMAINS = os.environ['INTERNAL_DOMAINS'].split(',')

    @classmethod
    def _es_dominio_interno(cls, mail):
        return mail.split('@')[1] in cls.INTERNAL_DOMAINS


    @classmethod
    def obtener_template(cls, template):
        templ = cls.env.get_template(template)
        return templ

    @classmethod
    def enviar_correo(cls, de, para, asunto, cuerpo):
        ''' https://developers.google.com/gmail/api/guides/sending '''
        bcuerpo = base64.urlsafe_b64encode(cuerpo.encode('utf-8')).decode()
        r = requests.post(cls.EMAILS_API_URL + '/correos/', json={'sistema':'users', 'de':de, 'para':para, 'asunto':asunto, 'cuerpo':bcuerpo})
        return r
