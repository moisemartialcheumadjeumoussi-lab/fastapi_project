



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from zope.interface.common import optional

app = FastAPI(title='Gestion Membre')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

class MembreBase (BaseModel):
    nom : str
    prenom: str
    email :EmailStr
    telephone: Optional[str] =None
    cotisation_payee : bool = False

class MembreCreate(MembreBase):
    pass

class Membre(MembreBase):
    id: int
    date_inscription: datetime

    class Config:
        from_attributes = True

# Base de données en mémoire
membres_db: List[Membre] = []
id_counter = 1

    # Routes
@app.get("/")
def root():
    return {"message": "API Gestion Node coworking"}

@app.post("/api/membres", response_model=Membre)
def creer_membre(membre: MembreCreate):
    global id_counter
    nouveau_membre = Membre(
        id=id_counter,
        **membre.dict(),
        date_inscription=datetime.now()
    )
    membres_db.append(nouveau_membre)
    id_counter += 1
    return nouveau_membre

@app.get("/api/membres", response_model=List[Membre])
def lire_membres(cotisation_payee: Optional[bool] = None):
    if cotisation_payee is not None:
        return [m for m in membres_db if m.cotisation_payee == cotisation_payee]
    return membres_db

@app.get("/api/membres/{membre_id}", response_model=Membre)
def lire_membre(membre_id: int):
    for membre in membres_db:
        if membre.id == membre_id:
            return membre
    raise HTTPException(status_code=404, detail="Membre non trouvé")

@app.put("/api/membres/{membre_id}", response_model=Membre)
def modifier_membre(membre_id: int, membre_data: MembreCreate):
    for i, membre in enumerate(membres_db):
        if membre.id == membre_id:
            membre_modifie = Membre(
                id=membre_id,
                **membre_data.dict(),
                date_inscription=membre.date_inscription
            )
            membres_db[i] = membre_modifie
            return membre_modifie
    raise HTTPException(status_code=404, detail="Membre non trouvé")

@app.delete("/api/membres/{membre_id}")
def supprimer_membre(membre_id: int):
    for i, membre in enumerate(membres_db):
        if membre.id == membre_id:
            membres_db.pop(i)
            return {"message": "Membre supprimé avec succès"}
    raise HTTPException(status_code=404, detail="Membre non trouvé")

@app.get("/api/stats")
def obtenir_stats():
    return {
        "total_membres": len(membres_db),
        "cotisations_payees": sum(1 for m in membres_db if m.cotisation_payee),
        "cotisations_impayees": sum(1 for m in membres_db if not m.cotisation_payee)
    }
membre1 = Membre("Martial","Moise","martialmoise99@gmail.com","078621891",True)
nouveau1 = creer_membre(membre1)

"""


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    nom: str
    description : str =None

items =[]

@app.post("/items", response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items")
def read_items():
    return items
@app.get("/items/{item_id}",response_model=Item)
def read_item(item_id:int):
    if item_id < len(items):
        return items[item_id]
    raise HTTPException(status_code=404,detail="il n'ya aucun items")

@app.delete("/items/{item_id}")
def delete_item(item_id:int):
    if item_id < len(items):
        return items.pop(item_id)
    raise HTTPException(status_code=404, detail="il n'ya aucun items")

item1 = create_item({"chien":"chiot"})
item2 = create_item({"chien":"chat"})
item3 = create_item({"chien":"souris"})"""