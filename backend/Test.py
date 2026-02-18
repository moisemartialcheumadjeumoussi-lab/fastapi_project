import sys
import os
from datetime import datetime

import pytest

from db import Database, membres_db, id_counter
from Membre import MembreCreate
from fastapi.testclient import TestClient
from main import app
import db


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
client = TestClient(app)


def setup_function():
    """Réinitialise la base avant chaque test"""
    db.membres_db.clear()
    db.id_counter = 0



def test_create_membre():
    membre_data = MembreCreate(
        nom="Dupont",
        prenom="Jean",
        email="jean@example.com",
        telephone="0600000000",
        cotisation_payee=True
    )

    membre = Database.create_membre(membre_data)

    assert membre.id == 0
    assert membre.nom == "Dupont"
    assert membre.telephone == "0600000000"
    assert membre.cotisation_payee is True
    assert isinstance(membre.date_inscription, datetime)
    assert len(membres_db) == 1



def test_get_all_membres():
    Database.create_membre(MembreCreate(
        nom="A", prenom="A", email="a@mail.com", telephone="0601010101", cotisation_payee=True
    ))
    Database.create_membre(MembreCreate(
        nom="B", prenom="B", email="b@mail.com", telephone="0602020202", cotisation_payee=False
    ))

    membres = Database.get_all_membres()

    assert len(membres) == 2
    assert membres[0].nom == "A"
    assert membres[1].nom == "B"


def test_get_membre_by_id():
    Database.create_membre(MembreCreate(
        nom="Test", prenom="User", email="test@mail.com", telephone="0603030303", cotisation_payee=True
    ))

    membre = Database.get_membre_by_id(0)

    assert membre is not None
    assert membre.nom == "Test"


def test_update_membre():
    Database.create_membre(MembreCreate(
        nom="Old", prenom="Name", email="old@mail.com", telephone="0604040404", cotisation_payee=False
    ))

    updated = Database.update_membre(0, MembreCreate(
        nom="New", prenom="Name", email="new@mail.com", telephone="0605050505", cotisation_payee=True
    ))

    assert updated is not None
    assert updated.nom == "New"
    assert updated.telephone == "0605050505"
    assert updated.cotisation_payee is True


def test_update_membre_not_found():
    updated = Database.update_membre(999, MembreCreate(
        nom="X", prenom="X", email="x@mail.com", telephone="0606060606", cotisation_payee=False
    ))

    assert updated is None


def test_delete_membre():
    Database.create_membre(MembreCreate(
        nom="Delete", prenom="Me", email="delete@mail.com", telephone="0607070707", cotisation_payee=False
    ))

    result = Database.delete_membre(0)

    assert result is True

    assert len(membres_db) == 0



def test_delete_membre_not_found():
    result = Database.delete_membre(123)
    assert result is False


def test_stats():
    Database.create_membre(MembreCreate(
        nom="A", prenom="A", email="a@mail.com", telephone="0608080808", cotisation_payee=True
    ))
    Database.create_membre(MembreCreate(
        nom="B", prenom="B", email="b@mail.com", telephone="0609090909", cotisation_payee=False
    ))

    stats = Database.get_stats()

    assert stats["total_membres"] == 2
    assert stats["cotisations_payees"] == 1
    assert stats["cotisations_impayees"] ==1












def test_post_membre1():

    response = client.post("/api/membres", json={
        "nom": "Jean",
        "prenom": "Dupont",
        "email": "jean@mail.com",
        "telephone": "0600000000",
        "cotisation_payee": True
    })

    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Jean"
    assert data["telephone"] == "0600000000"
    assert data["id"] == 0


def test_get_membres1():

    client.post("/api/membres", json={
        "nom": "A", "prenom": "A", "email": "a@mail.com", "telephone": "0601010101", "cotisation_payee": True
    })

    response = client.get("/api/membres")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_membre_by_id1():

    client.post("/api/membres", json={
        "nom": "Test", "prenom": "User", "email": "test@mail.com", "telephone": "0602020202", "cotisation_payee": True
    })

    response = client.get("/api/membres/0")
    assert response.status_code == 200
    assert response.json()["nom"] == "Test"


def test_update_membre1():

    client.post("/api/membres", json={
        "nom": "Old", "prenom": "Name", "email": "old@mail.com", "telephone": "0603030303", "cotisation_payee": False
    })

    response = client.put("/api/membres/0", json={
        "nom": "New", "prenom": "Name", "email": "new@mail.com", "telephone": "0604040404", "cotisation_payee": True
    })

    assert response.status_code == 200
    assert response.json()["nom"] == "New"


def test_delete_membre1():
    client.post("/api/membres", json={
        "nom": "Delete", "prenom": "Me", "email": "delete@mail.com", "telephone": "0605050505", "cotisation_payee": False
    })

    response = client.delete("/api/membres/0")
    assert response.status_code == 200

    # Vérifier qu'il n'existe plus
    response = client.get("/api/membres/0")
    assert response.status_code == 404



def test_stats1():
    client.post("/api/membres", json={
        "nom": "A", "prenom": "A", "email": "a@mail.com", "telephone": "0606060606", "cotisation_payee": True
    })
    client.post("/api/membres", json={
        "nom": "B", "prenom": "B", "email": "b@mail.com", "telephone": "0607070707", "cotisation_payee": False
    })

    response = client.get("/api/stats")
    assert response.status_code == 200
    stats = response.json()

    assert stats["total_membres"] == 2
    assert stats["cotisations_payees"] == 1
    assert stats["cotisations_impayees"] == 1

if __name__=='__main__':
    pytest.main(["-v","Test.py"])