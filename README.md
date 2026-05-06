# 🚲 Nantes Predict - Analyse et Prédiction des Flux Vélos

Ce projet vise à analyser et prédire l'affluence cycliste à Nantes (ex: Cours des 50 Otages) en croisant les données Open Data de Nantes Métropole avec des données météorologiques.

## 📂 Architecture du Projet

- ├── data/                     # Fichiers CSV bruts
- ├── velodata/                 # Module Python métier
- │   ├── __init__.py
- │   ├── data.py               # Script de téléchargement via API
- │   ├── fluxes.py             # Nettoyage et gestion des séries temporelles
- │   └── apimeteo.py           # Récupération des données météo (En cours)
- ├── velo_otages_predict.ipynb # Notebook
- ├── README.md
- └── .gitignore

## 🚀 Installation & Utilisation

1. Cloner le repository.
2. S'assurer que le dossier racine est dans le `PYTHONPATH` pour que les notebooks puissent importer le module `velodata`.
3. Lancer `velo_otages_predict.ipynb`
