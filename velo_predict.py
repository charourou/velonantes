import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split


# URL d'exportation complète (format CSV)
# J'ai reconstruit l'URL complète basée sur l'ID que vous avez fourni
url_csv = "https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/244400404_comptages-velo-nantes-metropole/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B"

print("Téléchargement des données en cours... ")

# %%  1. Chargement et nettoyage preliminaire
df = pd.read_csv(url_csv, sep=";")
print(df.columns)

# 2. Nettoyage préliminaire
# On renomme pour avoir des noms de colonnes faciles à manipuler
if 'Horodate' in df.columns:
    df['date'] = pd.to_datetime(df['Horodate'], utc=True)   # Conversion en format temporel
    df = df.set_index('date')                               # On met la date en index (axe X)

# %% 2 Exploration rapide
print(f"Nombre total de lignes : {len(df)}")
print("\n--- Les 5 premières lignes ---")
print(df.head())

# Filtrer sur UN seul compteur (Important !)
# Le fichier contient tous les compteurs de Nantes mélangés.
# Isolons un compteur emblématique, ex: "50 Otages"
# Listons d'abord les compteurs disponibles

print("\n--- Compteurs disponibles (Top 10) ---")
print(df['Numéro de boucle'].value_counts().head(10))
print(df['Boucle de comptage'].value_counts().head(10))

# Les passages les plus nombreux.
# - groupby('Libellé') : on "sépare" les données par nom de compteur
# - ['Total'] : on "isole" la colonne qui contient le nombre de vélos
# - .sum() : on "applique" l'addition et on "combine" le résultat
passages_par_compteur = df.groupby('Boucle de comptage')['Total'].sum()
classement = passages_par_compteur.sort_values(ascending=False)

# 3. Afficher les résultats
print("Le compteur le plus fréquenté est :", classement.index[0])
print(f"Avec un total de : {classement.iloc[0]:.0f} passages.\n")

print("--- Le Top 5 des compteurs nantais ---")
print(classement.head(5))

# %% 3 . Isolation d'un capteur.
# 786 - 50 Otages Vers Nord
compteur_cible = '786 - 50 Otages Vers Nord'
df_50_otages = df[df['Boucle de comptage'] == compteur_cible].copy()

# Vérifier que l'index est bien un format Date/Heure et le trier chronologiquement.
df_50_otages = df_50_otages.sort_index() # TODO


# Si le compteur a été éteint, il y a des negatifs ou des NaNs.
# Il y a aussi des valeurs exceptionnellements hautes.
# Ici, on remplace les valeurs manquantes par eds NaNs

# Masque sur les données horaires
# TODO

# Effectuer une somme pour retrouver un total.
# TODO

# Masque sur les valeurs totals.
df_50_otages.loc[df_50_otages['Total']<0,'Total'] = np.nan

mask = ~df['Probabilité de présence d\'anomalies'].isna()
df_50_otages.loc[mask,'Total'] = np.nan


# %% 4. Sauvegarder en local ---
# nom_fichier = 'dataset_50_otages_nettoye.csv'
# df_50_otages.to_csv(nom_fichier)
# print(f"✅ Fichier sauvegardé sous : {nom_fichier}\n")

# %% 5 - entrainement du modèle.

df_50_otages['mois'] = pd.to_datetime(df_50_otages['Date formatée']).dt.month
df_50_otages['congés'] = df_50_otages['Vacances'] != 'Hors Vacances'

predictor = df_50_otages[['Total','Jour de la semaine', 'mois','congés']]
predictor.dropna( axis = 0 , inplace = True)

# l'algorithme n'est pas capable de traiter les Booleans ??

model = KNeighborsRegressor()

X = predictor.drop('Total', axis= 1)
print(len(X))
y = predictor['Total']

X_train, X_test, y_train, y_test = train_test_split (X, y, test_size= 0.20)


model.fit(X_train, y_train)

# évaluation
print('score model:', model.score( X_test,  y_test ) )
# Mais l'erreur absolue moyenne (MAE) est plus parlante pour un industriel :
y_pred_test = model.predict(X_test)

# 2. Configuration de la taille de l'image
# alpha=0.6 rend les points semi-transparents pour voir où ils s'accumulent
plt.figure(figsize=(10, 8))
plt.scatter(y_test, y_pred_test, alpha=0.6, color='#005b96', edgecolor='white', s=60)
min_val = min(y_test.min(), y_pred_test.min())
max_val = max(y_test.max(), y_pred_test.max())

plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', linewidth=2, label='Prédiction parfaite (y = x)')

# 5. Esthétique et labels (Très important en entreprise)
plt.title('Performance du modèle : Passages Réels vs Prédits', fontsize=14, pad=15)
plt.xlabel('Vérité Terrain : Passages réels (y_test)', fontsize=12)
plt.ylabel('Estimation du Modèle : Passages prédits (y_pred_test)', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()








mae = mean_absolute_error(y_test, y_pred_test)
print(f"En moyenne, le modèle se trompe de {mae:.0f} vélos par jour.")

# --- 2. Tester un scénario inventé (La Prédiction) ---
# Imaginons que nous voulons prédire le trafic pour :
# - Un Mardi (supposons que Mardi = 2 ou 1 selon votre encodage)
# - Au mois d'Août (mois = 8)
# - Pendant les vacances (congés = True)

# Il faut recréer un DataFrame avec EXACTEMENT les mêmes colonnes que X
scenario = pd.DataFrame({
    'Jour de la semaine': [2], # Attention: si vos jours sont en texte ('Mardi'), il faudra les convertir en chiffres !
    'mois': [8],
    'congés': [True]
})

# La prédiction !
prediction = model.predict(scenario)
print(f"Prédiction pour ce jour d'août : {prediction[0]:.0f} passages de vélos.")

# %% tester le modèle

# %% . Commencer l'analyse ---

# Afficher les statistiques descriptives de base (Moyenne, Min, Max, Quartiles)
print("--- Statistiques descriptives du compteur ---")
print(df_50_otages.describe())

# Visualisation de la série temporelle
plt.figure(figsize=(15, 6))
plt.plot(df_50_otages.index, df_50_otages['Total'], color='#1f77b4', linewidth=0.8)
plt.title(f"Évolution des passages vélos - {compteur_cible}", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Nombre de passages (par heure/jour)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
