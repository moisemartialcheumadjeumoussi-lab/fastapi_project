from typing import List, Optional
from datetime import datetime
from Membre import Membre, MembreCreate


membres_db: List[Membre] = []
global id_counter


class Database:
    # Base de données en mémoire
    @staticmethod
    def get_all_membres() -> List[Membre]:
        """Récupère tous les membres, avec filtre optionnel sur cotisation_payee"""
        return [m for m in membres_db]

    @staticmethod
    def get_membre_by_id(membre_id: int) -> Optional[Membre]:
        """Récupère un membre par son ID"""
        for membre in membres_db:
            if membre.id == membre_id:
                return membre
        return None

    @staticmethod
    def create_membre(membre_data: MembreCreate) -> Membre:
        """Crée un nouveau membre"""
        global id_counter

        nouveau_membre = Membre(
            id=id_counter, **membre_data.dict(), date_inscription=datetime.now()
        )
        membres_db.append(nouveau_membre)
        id_counter += 1
        return nouveau_membre

    @staticmethod
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
                return membre_modifie
        return None

    @staticmethod
    def delete_membre(membre_id: int) -> bool:
        """Supprime un membre"""
        for i, membre in enumerate(membres_db):
            if membre.id == membre_id:
                membres_db.pop(i)
                return True
        return False

    @staticmethod
    def get_stats() -> dict:
        """Récupère les statistiques des membres"""
        return {
            "total_membres": len(membres_db),
            "cotisations_payees": sum(1 for m in membres_db if m.cotisation_payee),
            "cotisations_impayees": sum(
                1 for m in membres_db if not m.cotisation_payee
            ),
        }
