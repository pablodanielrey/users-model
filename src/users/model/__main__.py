

def create_tables():

    import os
    from sqlalchemy import create_engine

    from .entities import Base
    from .entities.User import User, Mail, Phone, File, IdentityNumber, UserDegree, UsersLog

    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['USERS_DB_USER'],
        os.environ['USERS_DB_PASSWORD'],
        os.environ['USERS_DB_HOST'],
        os.environ['USERS_DB_PORT'],
        os.environ['USERS_DB_NAME']
    ), echo=True)
    Base.metadata.create_all(engine)


create_tables()
