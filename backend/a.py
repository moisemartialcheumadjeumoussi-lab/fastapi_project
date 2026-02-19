from pygments.lexers import get_all_lexers

from db_sqlite import DatabaseSqlite
from Membre import MembreCreate
import datetime

db = DatabaseSqlite()
db.initialisation_de_la_db()
m = MembreCreate(nom="martial",prenom="moise",email="moisemartial@gmail.com",telephone="96296869",cotisation_payee=False)
db.create_membre(m)

b = db.get_all_membres()
print(b)


C = db.get_membre_by_id(999999)
print(C)

m1 = MembreCreate(nom="martial",prenom="moise",email="moisemartial@gmail.com",telephone="96296869",cotisation_payee=False)
g = MembreCreate(nom="moustique",prenom="jean_de_Dieu",email="moisemartial5@gmail.com",telephone="96296869",cotisation_payee=False)

membres = db.get_all_membres()
b = db.get_membre_by_id(membres[0].id)


a=db.update_membre(12,g)

e = db.get_stats()
print (e)



