
# Projet Access

## Présentation

Projet Access est une application web développée avec Django et PostgreSQL.

Ce dépôt contient le code source du projet. Ce guide explique comment installer et exécuter l'application localement après avoir récupéré le dépôt GitHub.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- Python 3.11 ou une version compatible avec le projet
- PostgreSQL
- pgAdmin 4
- Git
- Visual Studio Code (recommandé)

## 1. Récupération du projet

Ouvrir un terminal et exécuter :

```bash
git clone https://github.com/yeillenr/Projet-access
```

Accéder au dossier du projet :

```bash
cd "Projet access"
```

## 2. Configuration du Backend

Accéder au dossier backend :

```bash
cd backend
```

### Créer un environnement virtuel

```bash
python -m venv .venv
```

### Activer l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Sous Windows CMD :

```cmd
.venv\Scripts\activate.bat
```

Sous Linux ou macOS :

```bash
source .venv/bin/activate
```

### Installer les dépendances

Mettre pip à jour :

```bash
python -m pip install --upgrade pip
```

Installer les dépendances du projet :

```bash
pip install -r requirements.txt
```

## 3. Configuration de la base de données PostgreSQL

Le projet utilise PostgreSQL comme système de gestion de base de données. pgAdmin 4 permet de gérer la base de données graphiquement.

### Étape 1 : Créer une base de données

1. Ouvrir pgAdmin 4.
2. Se connecter à son serveur PostgreSQL.
3. Faire un clic droit sur Databases.
4. Sélectionner Create > Database.
5. Donner un nom à la base de données : `projet_access`.
6. Enregistrer.

### Étape 2 : Configurer la connexion

Créer un fichier `.env` dans le dossier `backend` et renseigner les paramètres de connexion :

```env
SECRET_KEY=votre_cle_secrete
DEBUG=True

DB_NAME=projet_access
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

Remplacer les valeurs par les informations correspondant à votre installation PostgreSQL.

**Important :** ne jamais publier le fichier `.env` sur GitHub.

## 4. Effectuer les migrations

Dans le terminal, toujours depuis le dossier `backend`, exécuter :

```bash
python manage.py makemigrations
python manage.py migrate
```

Ces commandes permettent de créer les tables nécessaires dans la base de données PostgreSQL.

## 5. Créer un compte administrateur

Pour accéder à l'administration Django :

```bash
python manage.py createsuperuser
```

Suivre les instructions affichées dans le terminal pour définir les identifiants.

## 6. Démarrer le serveur

Lancer le serveur de développement Django :

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse :

http://127.0.0.1:8000/

L'interface d'administration sera accessible à :

http://127.0.0.1:8000/admin/

## 7. Commandes utiles

| Commande | Description |
|---|---|
| `python manage.py runserver` | Démarrer le serveur Django |
| `python manage.py makemigrations` | Générer les migrations |
| `python manage.py migrate` | Appliquer les migrations |
| `python manage.py createsuperuser` | Créer un administrateur |
| `python manage.py check` | Vérifier la configuration Django |
| `pip install -r requirements.txt` | Installer les dépendances |

## Technologies utilisées

- Python
- Django
- PostgreSQL
- pgAdmin 4
