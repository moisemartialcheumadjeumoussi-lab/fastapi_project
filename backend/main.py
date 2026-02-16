from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from Membre import Membre, MembreCreate
from db import Database
#import SQLAlchemy

app = FastAPI(title='Gestion Membre')

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
    db = Database()
    return db



"""def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

@app.post("/api/membres", response_model=Membre)

def creer_membre(membre: MembreCreate,db: Database = Depends(get_database)):
    """Créer un nouveau membre"""
    return db.create_membre(membre)


@app.get("/api/membres", response_model=List[Membre])
def lire_membres(cotisation_payee: Optional[bool] = None,db: Database = Depends(get_database)):
    """Récupérer la liste des membres avec filtre optionnel"""
    return db.get_all_membres()


@app.get("/api/membres/{membre_id}", response_model=Membre)
def lire_membre(membre_id: int,db: Database = Depends(get_database)):
    return db.get_membre_by_id(membre_id)



@app.put("/api/membres/{membre_id}", response_model=Membre)
def modifier_membre(membre_id: int, membre_data: MembreCreate,db: Database = Depends(get_database)):
    """Modifier un membre existant"""
    membre_modifie = db.update_membre(membre_id, membre_data)
    if membre_modifie is None:
        raise HTTPException(status_code=404, detail="Membre non trouvé")
    return membre_modifie


@app.delete("/api/membres/{membre_id}")
def supprimer_membre(membre_id: int,db: Database = Depends(get_database)):
    """Supprimer un membre"""
    if not db.delete_membre(membre_id):
        raise HTTPException(status_code=404, detail="Membre non trouvé")
    return {"message": "Membre supprimé avec succès"}


@app.get("/api/stats")
def obtenir_stats(db: Database = Depends(get_database)):
    """Récupérer les statistiques des membres"""
    return db.get_stats()
