import sys
import os

import pytest
from Membre import MembreCreate
from fastapi.testclient import TestClient
from main import app

from db_sqlite import DatabaseSqlite

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
client = TestClient(app)

Data = DatabaseSqlite()
Data.initialisation_de_la_db()


def setup_function():

    Data.test_clear_db()


def test_create_membre():
    membre_data = MembreCreate(
        nom="Dupont",
        prenom="Jean",
        email="jean@example.com",
        telephone="0600000000",
        cotisation_payee=True,
    )

    membre = Data.create_membre(membre_data)
    assert membre.nom == "Dupont"
    assert membre.prenom == "Jean"
    assert membre.email == "jean@example.com"
    assert membre.telephone == "0600000000"
    assert membre.cotisation_payee is True


def test_get_all_membres():
    a1 = Data.create_membre(
        MembreCreate(
            nom="A",
            prenom="A",
            email="a@mail.com",
            telephone="0601010101",
            cotisation_payee=True,
        )
    )
    b1 = Data.create_membre(
        MembreCreate(
            nom="B",
            prenom="B",
            email="b@mail.com",
            telephone="0602020202",
            cotisation_payee=False,
        )
    )

    membres = Data.get_all_membres()

    assert len(membres) == 2
    assert membres[0].nom == a1.nom
    assert membres[1].nom == b1.nom


def test_get_membre_by_id():
    created = Data.create_membre(
        MembreCreate(
            nom="Test",
            prenom="User",
            email="test@mail.com",
            telephone="0603030303",
            cotisation_payee=True,
        )
    )

    member = Data.get_membre_by_id(created.id)

    assert member is not None
    assert member.nom == "Test"
    assert member.id == created.id


def test_update_membre():
    created = Data.create_membre(
        MembreCreate(
            nom="Old",
            prenom="Name",
            email="old@mail.com",
            telephone="0604040404",
            cotisation_payee=False,
        )
    )

    updated = Data.update_membre(
        created.id,
        MembreCreate(
            nom="New",
            prenom="Name",
            email="new@mail.com",
            telephone="0605050505",
            cotisation_payee=True,
        ),
    )

    assert updated is not None
    assert updated.nom == "New"
    assert updated.telephone == "0605050505"
    assert updated.cotisation_payee is True


def test_update_membre_not_found():
    updated = Data.update_membre(
        999,
        MembreCreate(
            nom="X",
            prenom="X",
            email="x@mail.com",
            telephone="0606060606",
            cotisation_payee=False,
        ),
    )

    assert updated is None


def test_delete_membre():
    created = Data.create_membre(
        MembreCreate(
            nom="Delete",
            prenom="Me",
            email="delete@mail.com",
            telephone="0607070707",
            cotisation_payee=False,
        )
    )

    result = Data.delete_membre(created.id)

    assert len(Data.get_all_membres()) == 0
    assert result is True


def test_delete_membre_not_found():
    result = Data.delete_membre(123)
    assert result is False


def test_stats():
    Data.create_membre(
        MembreCreate(
            nom="A",
            prenom="A",
            email="a@mail.com",
            telephone="0608080808",
            cotisation_payee=True,
        )
    )
    Data.create_membre(
        MembreCreate(
            nom="B",
            prenom="B",
            email="b@mail.com",
            telephone="0609090909",
            cotisation_payee=False,
        )
    )

    stats = Data.get_stats()

    assert stats["total_membres"] == 2
    assert stats["cotisations_payees"] == 1
    assert stats["cotisations_impayees"] == 1
