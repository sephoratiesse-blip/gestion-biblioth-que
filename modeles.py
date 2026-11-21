from dataclasses import dataclass
from typing import Optional


@dataclass
class Livre:
    id: int
    code: str
    titre: str
    auteur: str
    annee: int
    categorie: str
    disponible: bool


@dataclass
class Adherent:
    id: int
    matricule: str
    nom: str
    telephone: str


@dataclass
class Emprunt:
    id: int
    livre_id: int
    adherent_id: int
    date_emprunt: str
    date_retour_prevue: str
    date_retour_effective: Optional[str]