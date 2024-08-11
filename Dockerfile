FROM python:3.11-slim-buster

# Créer un répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt requirements.txt

# Installer les dépendances du projet
RUN pip install -r requirements.txt

# Copier le reste du code de l'application dans le répertoire de travail
COPY . .

# Définir le point d'entrée de l'application
CMD ["python", "run.py"]