NOM_APPLICATION = "BiblioIIT"
DUREE_EMPRUNT = 14
MAX_EMPRUNTS = 3
PENALITE_RETARD = 500
LIVRE_DISPONIBLE = "Disponible"
LIVRE_EMPRUNTE = "Emprunté"


def verifier_champ(valeur, nom_champ):
    if valeur is None or str(valeur).strip() == "":
        raise ValueError(f"Le champ {nom_champ} est obligatoire.")
    return str(valeur).strip()


def verifier_annee(annee):
    try:
        annee = int(annee)
        if annee < 1000 or annee > 2100:
            raise ValueError
        return annee
    except ValueError:
        raise ValueError("Veuillez saisir une année valide.")