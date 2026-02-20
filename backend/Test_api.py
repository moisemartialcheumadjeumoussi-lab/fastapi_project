import sys
import os

import pytest
from fastapi.testclient import TestClient
from main import app

from db_sqlite import DatabaseSqlite

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
client = TestClient(app)

Data = DatabaseSqlite()
Data.initialisation_de_la_db()


def setup_function():

    Data.test_clear_db()


def test_post_membre1():

    response = client.post(
        "/api/membres",
        json={
            "nom": "Jean",
            "prenom": "Dupont",
            "email": "jean@mail.com",
            "telephone": "0600000000",
            "cotisation_payee": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Jean"
    assert data["telephone"] == "0600000000"
    assert "id" in data


def test_get_membres1():

    client.post(
        "/api/membres",
        json={
            "nom": "A",
            "prenom": "A",
            "email": "a@mail.com",
            "telephone": "0601010101",
            "cotisation_payee": True,
        },
    )

    response = client.get("/api/membres")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_membre_by_id1():
    r = client.post(
        "/api/membres",
        json={
            "nom": "Test",
            "prenom": "User",
            "email": "test@mail.com",
            "telephone": "0602020202",
            "cotisation_payee": True,
        },
    )
    membre_id = r.json()["id"]

    response = client.get(f"/api/membres/{membre_id}")
    assert response.status_code == 200
    assert response.json()["nom"] == "Test"


def test_update_membre1():

    r = client.post(
        "/api/membres",
        json={
            "nom": "Old",
            "prenom": "Name",
            "email": "old@mail.com",
            "telephone": "0603030303",
            "cotisation_payee": False,
        },
    )
    membre_id = r.json()["id"]

    response = client.put(
        f"/api/membres/{membre_id}",
        json={
            "nom": "New",
            "prenom": "Name",
            "email": "new@mail.com",
            "telephone": "0604040404",
            "cotisation_payee": True,
        },
    )

    assert response.status_code == 200
    assert response.json()["nom"] == "New"


def test_delete_membre1():
    r = client.post(
        "/api/membres",
        json={
            "nom": "Delete",
            "prenom": "Me",
            "email": "delete@mail.com",
            "telephone": "0605050505",
            "cotisation_payee": False,
        },
    )
    membre_id = r.json()["id"]

    response = client.delete(f"/api/membres/{membre_id}")
    assert response.status_code == 200

    # Vérifier qu'il n'existe plus
    response = client.get(f"/api/membres/{membre_id}")
    assert response.status_code == 404


def test_stats1():
    client.post(
        "/api/membres",
        json={
            "nom": "A",
            "prenom": "A",
            "email": "a@mail.com",
            "telephone": "0606060606",
            "cotisation_payee": True,
        },
    )
    client.post(
        "/api/membres",
        json={
            "nom": "B",
            "prenom": "B",
            "email": "b@mail.com",
            "telephone": "0607070707",
            "cotisation_payee": False,
        },
    )

    response = client.get("/api/stats")
    assert response.status_code == 200
    stats = response.json()

    assert stats["total_membres"] == 2
    assert stats["cotisations_payees"] == 1
    assert stats["cotisations_impayees"] == 1


if __name__ == "__main__":
    pytest.main(["-v", "Test.py"])
