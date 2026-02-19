from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from Membre import Membre, MembreCreate
from db_sqlite import DatabaseSqlite

app = FastAPI(title="Gestion Membre")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
def root():
    return {"message": "API Gestion Node coworking"}


def get_database():
    db1 = DatabaseSqlite()
    db1.initialisation_de_la_db()

    return db1


"""def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""


@app.post("/api/membres", response_model=Membre)
def creer_membre(membre: MembreCreate,db1: DatabaseSqlite = Depends(get_database)):


    db1.create_membre(membre)
    membres = db1.get_all_membres()
    """Créer un nouveau membre"""
    return membres[-1]


@app.get("/api/membres", response_model=List[Membre])
def lire_membres(db1: DatabaseSqlite = Depends(get_database)):
    """Récupérer la liste des membres avec filtre optionnel"""
    return db1.get_all_membres()


@app.get("/api/membres/{membre_id}", response_model=Membre)
def lire_membre(membre_id: int,db1: DatabaseSqlite = Depends(get_database)):
    result1 = db1.get_membre_by_id(membre_id)
    if  not result1:
        raise HTTPException(status_code=404, detail="Membre non trouvé")
    return  result1


@app.put("/api/membres/{membre_id}", response_model=Membre)
def modifier_membre(
    membre_id: int, membre_data: MembreCreate,db1: DatabaseSqlite = Depends(get_database)
):
    """Modifier un membre existant"""
    membre_modifie1 = db1.update_membre(membre_id, membre_data)
    if  membre_modifie1 is None:
        raise HTTPException(status_code=404, detail="Membre non trouvé")
    return membre_modifie1


@app.delete("/api/membres/{membre_id}")
def supprimer_membre(membre_id: int,db1: DatabaseSqlite = Depends(get_database)):
    """Supprimer un membre"""
    if not db1.delete_membre(membre_id):
        raise HTTPException(status_code=404, detail="Membre non trouvé")
    return {"message": "Membre supprimé avec succès"}


@app.get("/api/stats")
def obtenir_stats(db1: DatabaseSqlite = Depends(get_database)):
    """Récupérer les statistiques des membres"""
    return db1.get_stats()
