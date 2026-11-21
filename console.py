import depot_sqlite as depot
import service
from regles import NOM_APPLICATION
from datetime import datetime


def afficher_livres(livres):
    if not livres:
        print("Aucun livre trouvé.")
        return

    for livre in livres:
        etat = "Disponible" if livre["disponible"] else "Emprunté"
        print(f'{livre["code"]} | {livre["titre"]} | {livre["auteur"]} | {etat}')


def ajouter_livre():
    service.ajouter_livre(
        input("Code : "),
        input("Titre : "),
        input("Auteur : "),
        input("Année : "),
        input("Catégorie : ")
    )
    print("Livre ajouté avec succès.")


def inscrire_adherent():
    service.ajouter_adherent(
        input("Matricule : "),
        input("Nom : "),
        input("Téléphone : ")
    )
    print("Adhérent inscrit avec succès.")


def emprunter_livre():
    code = input("Code du livre : ")
    matricule = input("Matricule de l'adhérent : ")

    date_emprunt = input("Date d'emprunt (JJ/MM/AAAA) : ")

    while True:
        date_retour = input("Date de retour prévue (JJ/MM/AAAA) : ")

        try:
            debut = datetime.strptime(date_emprunt, "%d/%m/%Y")
            fin = datetime.strptime(date_retour, "%d/%m/%Y")

            duree = (fin - debut).days

            if duree <= 0:
                print("La date de retour doit être après la date d'emprunt.")
                continue

            if duree > 14:
                print("Date de retour invalide !")
                print("La durée maximale d'un emprunt est de 14 jours.")
                print("Veuillez saisir une date dans un délai de 14 jours.")
                continue

            break

        except ValueError:
            print("Format de date invalide. Utilisez JJ/MM/AAAA.")

    debut, fin = service.emprunter(
        code, matricule, date_emprunt, date_retour
    )

    print("\nEmprunt enregistré avec succès.")
    print("Date d'emprunt :", debut.strftime("%d/%m/%Y"))
    print("Date de retour prévue :", fin.strftime("%d/%m/%Y"))


def rendre_livre():
    code = input("Code du livre : ")
    matricule = input("Matricule de l'adhérent : ")

    jours, penalite, date_prevue, date_effective = service.rendre(
        code, matricule
    )

    print("\n===== RETOUR DU LIVRE =====")
    print("Date de retour prévue :", date_prevue.strftime("%d/%m/%Y"))
    print("Date de retour effective :", date_effective.strftime("%d/%m/%Y"))

    if jours > 0:
        print("STATUT : ADHÉRENT EN RETARD")
        print("Nombre de jours de retard :", jours)
        print("Pénalité à payer :", penalite, "FCFA")
    else:
        print("STATUT : RETOUR EFFECTUÉ SANS RETARD")
        print("Aucune pénalité à payer.")


def consulter_retards():
    retards = service.consulter_retards()

    print("\n===== LIVRES EN RETARD =====")

    if not retards:
        print("Aucun retard actuellement.")
        return

    for emprunt, jours, penalite in retards:
        print(f'Livre : {emprunt["titre"]}')
        print(f'Adhérent : {emprunt["nom"]}')
        print(f"Jours de retard : {jours}")
        print(f"Pénalité à payer : {penalite} FCFA")
        print("------------------------------")


def afficher_statistiques():
    stats = depot.statistiques()

    print("\n===== STATISTIQUES =====")
    print(f'Nombre de livres : {stats["livres"]}')
    print(f'Livres disponibles : {stats["disponibles"]}')
    print(f'Nombre d’adhérents : {stats["adherents"]}')
    print(f'Emprunts en cours : {stats["emprunts"]}')


def menu():
    print(f"""
========== {NOM_APPLICATION} ==========

1. Ajouter un livre
2. Rechercher un livre
3. Afficher les livres
4. Inscrire un adhérent
5. Emprunter un livre
6. Rendre un livre
7. Consulter les retards
8. Statistiques
0. Quitter

=======================================
""")


def main():
    depot.initialiser_base()

    while True:
        menu()
        choix = input("Votre choix : ").strip()

        print("Choix reçu :", choix)

        try:
            if choix == "1":
                ajouter_livre()

            elif choix == "2":
                terme = input("Recherche : ")
                afficher_livres(service.rechercher(terme))

            elif choix == "3":
                print("\n===== LISTE DES LIVRES =====")
                afficher_livres(depot.lister_livres())

            elif choix == "4":
                inscrire_adherent()

            elif choix == "5":
                emprunter_livre()

            elif choix == "6":
                rendre_livre()

            elif choix == "7":
                consulter_retards()

            elif choix == "8":
                afficher_statistiques()

            elif choix == "0":
                print("Au revoir !")
                break

            else:
                print("Choix invalide.")

        except Exception as erreur:
            print("Erreur :", erreur)

        if choix != "0":
            input("\nAppuie sur Entrée pour revenir au menu...")


if __name__ == "__main__":
    main()