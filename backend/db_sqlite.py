import sqlite3
from typing import List, Optional
from datetime import datetime
from Membre import Membre, MembreCreate

DB_PATH = "membres.db"
id_counter: int = 0











def sauvegarder_membre(membre: Membre):
    """Sauvegarde un membre dans SQLite (insertion ou mise à jour)"""
    with get_connection() as conn:
        # Vérifier si le membre existe déjà
        existing = conn.execute("SELECT id FROM membres WHERE id = ?", (membre.id,)).fetchone()

        if existing:
            # Mise à jour
            conn.execute("""
                         UPDATE membres
                         SET nom=?,
                             prenom=?,
                             email=?,
                             telephone=?,
                             cotisation_payee=?,
                             date_inscription=?
                         WHERE id = ?
                         """, (
                             membre.nom, membre.prenom, membre.email, membre.telephone,
                             int(membre.cotisation_payee), membre.date_inscription.isoformat(),
                             membre.id
                         ))
        else:
            # Insertion
            conn.execute("""
                         INSERT INTO membres (id, nom, prenom, email, telephone, cotisation_payee, date_inscription)
                         VALUES (?, ?, ?, ?, ?, ?, ?)
                         """, (
                             membre.id, membre.nom, membre.prenom, membre.email, membre.telephone,
                             int(membre.cotisation_payee), membre.date_inscription.isoformat()
                         ))

        conn.commit()


def supprimer_membre_db(membre_id: int):
    """Supprime un membre de SQLite"""
    with get_connection() as conn:
        conn.execute("DELETE FROM membres WHERE id = ?", (membre_id))
        conn.commit()


class DatabaseSqlite:
    # Base de données en mémoire

    def __init__(self):
        self.conn = sqlite3.connect('membres.db')
        self.conn.row_factory = sqlite3.Row

    #with self.conn permet de faire une transactions   https://www.bing.com/ck/a?!&&p=9d3352a9c16fff9eccf428167104aad132fdb852ba024db351c65312c034000eJmltdHM9MTc3MTM3MjgwMA&ptn=3&ver=2&hsh=4&fclid=1d48ab87-1db1-6619-07ce-bd711c8b67d5&psq=sqlite+begin+transaction&u=a1aHR0cHM6Ly93d3cuc3FsaXRldHV0b3JpYWwubmV0L3NxbGl0ZS10cmFuc2FjdGlvbi8
    def initialisation_de_la_db(self):
        with self.conn as conn:
            conn.execute("""
                         CREATE TABLE IF NOT EXISTS membres
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             nom
                             TEXT
                             NOT
                             NULL,
                             prenom
                             TEXT
                             NOT
                             NULL,
                             email
                             TEXT
                             NOT
                             NULL,
                             telephone
                             TEXT,
                             cotisation_payee
                             INTEGER
                             NOT
                             NULL
                             DEFAULT
                             0,
                             date_inscription
                             TEXT

                         )""")

            conn.commit()




    def get_all_membres(self) -> List[Membre]:
         with self.conn as conn:
             l =[]

             cursor = conn.cursor()
             cursor.execute("SELECT * FROM membres ")
             rows=cursor.fetchall()
             for row in rows:
                 m = Membre(id=row["id"],nom=row["nom"],prenom=row["prenom"],email=row["email"],telephone=row["telephone"],cotisation_payee=row["cotisation_payee"],date_inscription=row["date_inscription"])
                 l.append(m)
             print(l)


         return l


    def get_membre_by_id(self,membre_id: int) -> Optional[Membre]:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM membres WHERE id=?",(membre_id,))
            row = cursor.fetchone()
            if not row :
                return None
            m = Membre(id=row["id"], nom=row["nom"], prenom=row["prenom"], email=row["email"],
                           telephone=row["telephone"], cotisation_payee=row["cotisation_payee"],
                           date_inscription=row["date_inscription"])

        return m


    def create_membre(self, membre: MembreCreate):
        with self.conn as conn:
            date_inscription=datetime.now()
            conn.execute("""
                         INSERT INTO membres (nom, prenom, email, telephone, cotisation_payee, date_inscription)
                         VALUES ( ?, ?, ?, ?, ?, ?)
                         """, (
                              membre.nom, membre.prenom, membre.email, membre.telephone,
                             int(membre.cotisation_payee), date_inscription.isoformat()
                         ))

            conn.commit()



    def update_membre(membre_id: int, membre_data: MembreCreate) -> Optional[Membre]:
        """Met à jour un membre existant"""
        for i, membre in enumerate(membres_db):
            if membre.id == membre_id:
                membre_modifie = Membre(
                    id=membre_id,
                    **membre_data.dict(),
                    date_inscription=membre.date_inscription
                )
                membres_db[i] = membre_modifie
                sauvegarder_membre(membre_modifie)
                return membre_modifie
        return None


    def delete_membre(membre_id: int) -> bool:
        """Supprime un membre"""
        for i, membre in enumerate(membres_db):
            if membre.id == membre_id:
                membres_db.pop(i)
                supprimer_membre_db(membre_id)
                return True
        return False


    def get_stats() -> dict:
        """Récupère les statistiques des membres"""
        return {
            "total_membres": len(membres_db),
            "cotisations_payees": sum(1 for m in membres_db if m.cotisation_payee),
            "cotisations_impayees": sum(1 for m in membres_db if not m.cotisation_payee)
        }
