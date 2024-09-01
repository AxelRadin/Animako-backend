#!/bin/bash

# Définir le nom du fichier de log avec la date et l'heure
LOG_FILE="/home/axel/Animako-backend-log/deploy_$(date +'%Y%m%d_%H%M%S').log"

# Activer le mode xtrace pour loguer chaque commande exécutée
set -x

# Rediriger les sorties standard et d'erreur vers le fichier de log
exec &> >(tee -a "$LOG_FILE")

echo "Début du déploiement..."

# Aller dans le répertoire de votre application 
cd /home/axel/Animako-backend

# Puller les mises à jour
git pull origin main

# Creer un environnement virtuel
virtualenv env -p python3

# Activer l'environnement virtuel
source /home/axel/Animako-backend/env/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Exécuter les migrations
python manage.py makemigrations
python manage.py migrate

# Redémarrer le service via Supervisor
sudo -S supervisorctl restart animako-backend-gunicorn


echo "Déploiement terminé."

# Désactiver le mode xtrace
set +x