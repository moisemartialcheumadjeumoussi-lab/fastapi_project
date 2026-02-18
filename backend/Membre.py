from pydantic import BaseModel,ConfigDict, EmailStr
from datetime import datetime
from typing import Optional


class MembreCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    cotisation_payee: bool = False


class Membre(BaseModel):

    id: int
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    cotisation_payee: bool = False
    date_inscription: datetime

    class Config:
        from_attributes = True
