from datetime import date, datetime
import sqlite3
import depot_sqlite as depot
from regles import MAX_EMPRUNTS, PENALITE_RETARD, DUREE_EMPRUNT, verifier_champ, verifier_annee


def convertir_date(valeur, nom):
    try:
        return datetime.strptime(valeur.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise ValueError(f"{nom} invalide. Utilisez JJ/MM/AAAA.")


def ajouter_livre(code, titre, auteur, annee, categorie):
    code = verifier_champ(code, "code").upper()
    titre = verifier_champ(titre, "titre")
    auteur = verifier_champ(auteur, "auteur")
    categorie = verifier_champ(categorie, "catégorie")
    annee = verifier_annee(annee)

    try:
        depot.ajouter_livre(code, titre, auteur, annee, categorie)
    except sqlite3.IntegrityError:
        raise ValueError("Ce code de livre existe déjà.")


def ajouter_adherent(matricule, nom, telephone):
    matricule = verifier_champ(matricule, "matricule").upper()
    nom = verifier_champ(nom, "nom")
    telephone = verifier_champ(telephone, "téléphone")

    try:
        depot.ajouter_adherent(matricule, nom, telephone)
    except sqlite3.IntegrityError:
        raise ValueError("Ce matricule existe déjà.")


def rechercher(terme):
    terme = verifier_champ(terme, "recherche")
    return depot.rechercher_livre(terme)


def emprunter(code, matricule, date_emprunt_saisie, date_retour_saisie):
    code = verifier_champ(code, "code").upper()
    matricule = verifier_champ(matricule, "matricule").upper()

    date_emprunt = convertir_date(date_emprunt_saisie, "Date d'emprunt")
    date_retour = convertir_date(date_retour_saisie, "Date de retour")

    if date_retour <= date_emprunt:
        raise ValueError("La date de retour doit être après la date d'emprunt.")

    duree = (date_retour - date_emprunt).days

    if duree > DUREE_EMPRUNT:
        raise ValueError(
            f"La durée maximale d'un emprunt est de {DUREE_EMPRUNT} jours. "
            f"Veuillez choisir une date de retour dans ce délai."
        )

    livre = depot.trouver_livre(code)
    adherent = depot.trouver_adherent(matricule)

    if livre is None:
        raise ValueError("Livre introuvable.")

    if adherent is None:
        raise ValueError("Adhérent introuvable.")

    if not livre["disponible"]:
        raise ValueError("Ce livre est déjà emprunté.")

    if depot.nombre_emprunts(adherent["id"]) >= MAX_EMPRUNTS:
        raise ValueError("Limite d'emprunts atteinte.")

    depot.enregistrer_emprunt(
        livre["id"],
        adherent["id"],
        date_emprunt.isoformat(),
        date_retour.isoformat()
    )

    return date_emprunt, date_retour


def rendre(code, matricule):
    code = verifier_champ(code, "code").upper()
    matricule = verifier_champ(matricule, "matricule").upper()

    emprunt = depot.emprunt_actif(code, matricule)

    if emprunt is None:
        raise ValueError("Aucun emprunt actif trouvé.")

    aujourd_hui = date.today()

    date_prevue = date.fromisoformat(emprunt["date_retour_prevue"])

    jours_retard = max(0, (aujourd_hui - date_prevue).days)
    penalite = jours_retard * PENALITE_RETARD

    depot.enregistrer_retour(
        emprunt["id"],
        emprunt["livre_id"],
        aujourd_hui.isoformat()
    )

    return jours_retard, penalite, date_prevue, aujourd_hui


def consulter_retards():
    aujourd_hui = date.today()
    emprunts = depot.lister_retards(aujourd_hui.isoformat())

    resultats = []

    for emprunt in emprunts:
        date_prevue = date.fromisoformat(emprunt["date_retour_prevue"])
        jours = (aujourd_hui - date_prevue).days
        penalite = jours * PENALITE_RETARD
        resultats.append((emprunt, jours, penalite))

    return resultats