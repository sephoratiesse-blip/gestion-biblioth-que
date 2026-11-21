# BiblioIIT – Application de gestion de bibliothèque

## 1. Présentation du projet

BiblioIIT est une application console développée en Python permettant de faciliter la gestion d'une bibliothèque.

Elle permet de gérer les livres, les adhérents, les emprunts et les retours. Les informations sont enregistrées dans une base de données SQLite afin d'assurer leur conservation.

## 2. Fonctionnalités principales

L'application propose les fonctionnalités suivantes :

- Ajouter un livre.
- Rechercher un livre.
- Afficher la liste des livres.
- Inscrire un nouvel adhérent.
- Enregistrer l'emprunt d'un livre.
- Enregistrer le retour d'un livre.
- Consulter les livres en retard.
- Afficher les statistiques de la bibliothèque.

## 3. Technologies utilisées

- **Python** : langage de programmation utilisé pour développer l'application.
- **SQLite** : système de gestion de base de données utilisé pour stocker les informations.
- **VS Code** : environnement de développement utilisé pour réaliser le projet.

## 4. Structure du projet

```text
gestion_bibliothèque/
│
├── console.py
├── service.py
├── depot_sqlite.py
├── modeles.py
├── regles.py
│
├── data/
│   └── bibliotheque.db
│
├── .venv/
│
└── README.md
```

### Rôle des fichiers

- **console.py** : gère l'affichage du menu et les interactions avec l'utilisateur.
- **service.py** : contient les fonctions qui assurent le traitement des opérations de la bibliothèque.
- **depot_sqlite.py** : gère la connexion à la base de données et les opérations SQL.
- **modeles.py** : regroupe les modèles utilisés dans l'application.
- **regles.py** : contient les règles de gestion et les constantes du projet.
- **data/bibliotheque.db** : contient les données enregistrées dans la base de données.

## 5. Installation et configuration

### Prérequis

- Python installé sur l'ordinateur.
- Visual Studio Code.

### Création de l'environnement virtuel

Dans le terminal du projet, exécuter :

```bash
python -m venv .venv
```

### Activation de l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Si l'exécution des scripts est bloquée, utiliser :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Puis réactiver l'environnement virtuel.

## 6. Lancement de l'application

Une fois l'environnement virtuel activé, exécuter la commande :

```bash
python console.py
```

Le menu principal de BiblioIIT s'affiche alors dans le terminal.

## 7. Règles de gestion

L'application respecte les règles suivantes :

- Un livre ne peut pas être emprunté s'il est déjà emprunté.
- Un adhérent peut effectuer au maximum **3 emprunts simultanés**.
- La durée maximale d'un emprunt est de **14 jours**.
- La date de retour doit obligatoirement être postérieure à la date d'emprunt.
- Les dates d'emprunt et de retour prévue sont saisies manuellement.
- Si la durée saisie dépasse 14 jours, l'application demande à l'utilisateur de choisir une date de retour respectant le délai autorisé.
- Un retard entraîne une pénalité de **500 FCFA par jour**.
- Lorsqu'un livre est rendu, sa disponibilité est automatiquement mise à jour.

## 8. Base de données

La base de données SQLite est composée de trois tables principales :

### Table livres

Elle contient les informations relatives aux livres :

- Identifiant
- Code du livre
- Titre
- Auteur
- Année de publication
- Catégorie
- Disponibilité

### Table adherents

Elle contient les informations relatives aux adhérents :

- Identifiant
- Matricule
- Nom
- Téléphone

### Table emprunts

Elle permet de suivre les emprunts et les retours :

- Identifiant
- Identifiant du livre
- Identifiant de l'adhérent
- Date d'emprunt
- Date de retour prévue
- Date de retour effective

## 9. Conclusion

BiblioIIT est une application conçue pour simplifier la gestion quotidienne d'une bibliothèque. Elle permet d'organiser les informations sur les livres et les adhérents, de suivre les emprunts et les retours, et de contrôler les retards grâce à une base de données SQLite.