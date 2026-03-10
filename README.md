
# LitReview

LitReview est une application web Django permettant de créer, partager et gérer des tickets de demande de critique de livres, ainsi que de publier des critiques. Elle intègre un système d'authentification, de gestion des abonnements entre utilisateurs, et un flux d'actualités personnalisé.

## Fonctionnalités principales
- Inscription et authentification des utilisateurs
- Création, modification et suppression de tickets (demandes de critique)
- Création, modification et suppression de critiques
- Réponse à un ticket par une critique
- Abonnement/désabonnement à d'autres utilisateurs
- Flux personnalisé (tickets et critiques des abonnements)

## Structure du projet
```
LitReview/
├── authentification/   # Gestion des utilisateurs et abonnements
├── feed/               # Flux d'actualités personnalisé
├── reviews/            # Gestion des tickets et critiques
├── litreview/          # Paramètres et configuration Django
├── static/             # Fichiers statiques (CSS, images)
├── templates/          # Templates HTML globaux
├── db.sqlite3          # Base de données SQLite (dev)
├── manage.py           # Commandes Django
├── requirements.txt    # Dépendances Python
```

## Installation
1. **Cloner le dépôt**
	```bash
	git clone <url-du-repo>
	cd LitReview
	```
2. **Créer un environnement virtuel**
	```bash
	python -m venv venv
	source venv/bin/activate  # ou venv\Scripts\activate sous Windows
	```
3. **Installer les dépendances**
	```bash
	pip install -r requirements.txt
	```
4. **Appliquer les migrations**
	```bash
	python manage.py migrate
	```
5. **Créer un superutilisateur (optionnel)**
	```bash
	python manage.py createsuperuser
	```
6. **Lancer le serveur de développement**
	```bash
	python manage.py runserver
	```

## Utilisation
- Accéder à l'application via [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- S'inscrire, se connecter, créer des tickets et des critiques, suivre d'autres utilisateurs, etc.

## Dépendances principales
- Django==6.0.2
- pillow

Voir `requirements.txt` pour la liste complète.

## Tests et qualité du code
- Pour vérifier la conformité PEP8 :
  ```bash
  flake8 . --exclude=venv,.venv,env,.env,__pycache__,migrations
  ```
- Pour générer un rapport HTML flake8 :
  ```bash
  flake8 . --format=html --htmldir=flake8-html-report
  ```

## Auteur
Projet réalisé dans le cadre d'une formation OpenClassrooms.

---
N'hésitez pas à adapter ce README selon vos besoins spécifiques ou à ajouter des sections (FAQ, contribution, licence, etc.).
