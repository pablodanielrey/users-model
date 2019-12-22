import sys
import psycopg2

from users.model import open_session
from users.model.UsersModel import UsersModel
from users.model.entities.User import User, PersonNumberTypes

persons = []

dsn = sys.argv[1]
con = psycopg2.connect(dsn=dsn)
try:
    cur = con.cursor()
    try:
        cur.execute('select p.pers_nombres, p.pers_apellidos, p.pers_nrodoc, p.pers_fecha_nacimiento, e.empleado_cuil from empleado e left join persona p on (e.empleado_pers_id = p.pers_id)')
        for p in cur:
            persons.append({
                'n':p[0],
                'a':p[1],
                'd':p[2],
                'f':p[3],
                'c':p[4]
            })

    finally:
        cur.close()
finally:
    con.close()


with open_session() as session:
    for p in persons:
        try:
            dni = p['d'].strip()
            user = UsersModel.get_uid_person_number(session, dni)
            if not user:
                print(f"agregando persona {p['n']} {p['a']} {p['d']}")
                u = User()
                u.firstname = p['n']
                u.lastname = p['a']
                u.person_number = p['d']
                u.person_number_type = PersonNumberTypes.DNI
                u.birthdate = p['f']
                session.add(u)
                session.commit()

        except Exception as e:
            print(e)

