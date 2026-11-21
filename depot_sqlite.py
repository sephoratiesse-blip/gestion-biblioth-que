import sqlite3
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
CHEMIN_BD = DOSSIER / "data" / "bibliotheque.db"


def connexion():
    CHEMIN_BD.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(CHEMIN_BD)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialiser_base():
    with connexion() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS livres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                annee INTEGER NOT NULL,
                categorie TEXT NOT NULL,
                disponible INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS adherents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT UNIQUE NOT NULL,
                nom TEXT NOT NULL,
                telephone TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS emprunts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livre_id INTEGER NOT NULL,
                adherent_id INTEGER NOT NULL,
                date_emprunt TEXT NOT NULL,
                date_retour_prevue TEXT NOT NULL,
                date_retour_effective TEXT,
                FOREIGN KEY(livre_id) REFERENCES livres(id),
                FOREIGN KEY(adherent_id) REFERENCES adherents(id)
            );
        """)


def ajouter_livre(code, titre, auteur, annee, categorie):
    with connexion() as conn:
        conn.execute("""
            INSERT INTO livres(code, titre, auteur, annee, categorie)
            VALUES (?, ?, ?, ?, ?)
        """, (code, titre, auteur, annee, categorie))


def ajouter_adherent(matricule, nom, telephone):
    with connexion() as conn:
        conn.execute("""
            INSERT INTO adherents(matricule, nom, telephone)
            VALUES (?, ?, ?)
        """, (matricule, nom, telephone))


def lister_livres():
    with connexion() as conn:
        return conn.execute(
            "SELECT * FROM livres ORDER BY titre"
        ).fetchall()


def rechercher_livre(terme):
    recherche = f"%{terme}%"
    with connexion() as conn:
        return conn.execute("""
            SELECT * FROM livres
            WHERE titre LIKE ? OR auteur LIKE ?
            OR code LIKE ? OR categorie LIKE ?
        """, (recherche, recherche, recherche, recherche)).fetchall()


def trouver_livre(code):
    with connexion() as conn:
        return conn.execute(
            "SELECT * FROM livres WHERE code = ?", (code,)
        ).fetchone()


def trouver_adherent(matricule):
    with connexion() as conn:
        return conn.execute(
            "SELECT * FROM adherents WHERE matricule = ?", (matricule,)
        ).fetchone()


def nombre_emprunts(adherent_id):
    with connexion() as conn:
        return conn.execute("""
            SELECT COUNT(*) FROM emprunts
            WHERE adherent_id = ?
            AND date_retour_effective IS NULL
        """, (adherent_id,)).fetchone()[0]


def enregistrer_emprunt(livre_id, adherent_id, date_emprunt, date_retour):
    with connexion() as conn:
        conn.execute(
            "UPDATE livres SET disponible = 0 WHERE id = ?",
            (livre_id,)
        )
        conn.execute("""
            INSERT INTO emprunts(
                livre_id, adherent_id,
                date_emprunt, date_retour_prevue
            )
            VALUES (?, ?, ?, ?)
        """, (livre_id, adherent_id, date_emprunt, date_retour))


def emprunt_actif(code, matricule):
    with connexion() as conn:
        return conn.execute("""
            SELECT emprunts.*, livres.id AS livre_id
            FROM emprunts
            JOIN livres ON livres.id = emprunts.livre_id
            JOIN adherents ON adherents.id = emprunts.adherent_id
            WHERE livres.code = ?
            AND adherents.matricule = ?
            AND emprunts.date_retour_effective IS NULL
        """, (code, matricule)).fetchone()


def enregistrer_retour(emprunt_id, livre_id, date_retour):
    with connexion() as conn:
        conn.execute("""
            UPDATE emprunts
            SET date_retour_effective = ?
            WHERE id = ?
        """, (date_retour, emprunt_id))

        conn.execute(
            "UPDATE livres SET disponible = 1 WHERE id = ?",
            (livre_id,)
        )


def lister_retards(aujourdhui):
    with connexion() as conn:
        return conn.execute("""
            SELECT emprunts.*, livres.titre,
                   adherents.nom, adherents.matricule
            FROM emprunts
            JOIN livres ON livres.id = emprunts.livre_id
            JOIN adherents ON adherents.id = emprunts.adherent_id
            WHERE emprunts.date_retour_effective IS NULL
            AND emprunts.date_retour_prevue < ?
        """, (aujourdhui,)).fetchall()


def statistiques():
    with connexion() as conn:
        return {
            "livres": conn.execute(
                "SELECT COUNT(*) FROM livres"
            ).fetchone()[0],

            "disponibles": conn.execute(
                "SELECT COUNT(*) FROM livres WHERE disponible = 1"
            ).fetchone()[0],

            "adherents": conn.execute(
                "SELECT COUNT(*) FROM adherents"
            ).fetchone()[0],

            "emprunts": conn.execute("""
                SELECT COUNT(*) FROM emprunts
                WHERE date_retour_effective IS NULL
            """).fetchone()[0]
        }