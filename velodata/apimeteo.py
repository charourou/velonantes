'''
 Example of a Python implementation for a continuous authentication client.
API MeteoFrance

The target is to transform the initial script into a class ApiMeteo and workable methods.

'''

import requests, time
import pandas as pd

from velodata.data import VeloData


class ApiMeteo:
    """
    A class to deal with the API at meteo France.

    The goal is to create and concatenate data into dataframes
    Daily meteorological information.

    """

    def get_key(self):
        """
        Fetches the user for a valid API_KEY.
        """
        pass

    def verify_key(self):
        """
        Checks the key is valid
        """
        pass

    def one_request(self, year = 2022 ):
        """
        Constructs dynamically the debut_api, fin_api, and then the url_commande.
        Sends the request for one year of data.

        Prints the response for that commande

        """
        url_fichier = '' # TO BE IMPLEMENTED
        return url_fichier

    def download(self, url_fichier : str):
        """
        Downloads the file on the url_fichier after a 10 second waiting

        prints out error messages if any.

        return a dataframe with key features ONLY
        transforms the following features:
            - AAAAMMJJ : index (as timestamp type I guess)
            - RR : prec
            - TX : tmax
            - FF2M : Vave

        date as index for the dataframe
        """
        return pd.DataFrame([])





# intial script
# 1. Configuration initiale
API_KEY = "eyJ4NXQiOiJZV0kxTTJZNE1qWTNOemsyTkRZeU5XTTRPV014TXpjek1UVmhNbU14T1RSa09ETXlOVEE0Tnc9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJtYXhpbWUucmljaGFyZDQ0QGNhcmJvbi5zdXBlciIsImFwcGxpY2F0aW9uIjp7Im93bmVyIjoibWF4aW1lLnJpY2hhcmQ0NCIsInRpZXJRdW90YVR5cGUiOm51bGwsInRpZXIiOiJVbmxpbWl0ZWQiLCJuYW1lIjoiRGVmYXVsdEFwcGxpY2F0aW9uIiwiaWQiOjM5ODMwLCJ1dWlkIjoiZWMyYTc3OGUtMDNhZi00MTc2LWE5Y2EtNzE0NTYwZjE1M2EyIn0sImlzcyI6Imh0dHBzOlwvXC9wb3J0YWlsLWFwaS5tZXRlb2ZyYW5jZS5mcjo0NDNcL29hdXRoMlwvdG9rZW4iLCJ0aWVySW5mbyI6eyI1MFBlck1pbiI6eyJ0aWVyUXVvdGFUeXBlIjoicmVxdWVzdENvdW50IiwiZ3JhcGhRTE1heENvbXBsZXhpdHkiOjAsImdyYXBoUUxNYXhEZXB0aCI6MCwic3RvcE9uUXVvdGFSZWFjaCI6dHJ1ZSwic3Bpa2VBcnJlc3RMaW1pdCI6MCwic3Bpa2VBcnJlc3RVbml0Ijoic2VjIn19LCJrZXl0eXBlIjoiUFJPRFVDVElPTiIsInN1YnNjcmliZWRBUElzIjpbeyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6IkRvbm5lZXNQdWJsaXF1ZXNDbGltYXRvbG9naWUiLCJjb250ZXh0IjoiXC9wdWJsaWNcL0RQQ2xpbVwvdjEiLCJwdWJsaXNoZXIiOiJhZG1pbl9tZiIsInZlcnNpb24iOiJ2MSIsInN1YnNjcmlwdGlvblRpZXIiOiI1MFBlck1pbiJ9XSwiZXhwIjoxNzc3NDgwMzg3LCJ0b2tlbl90eXBlIjoiYXBpS2V5IiwiaWF0IjoxNzc3NDc0Mzg3LCJqdGkiOiJjMjNhYzAwNC0zM2I3LTQwZGEtODQ1My0wMmJkYjE2MzZjZmEifQ==.ErCmmrMUrinGm2H3Cc_nqiQXjjYZ2SlCVcen4waer2VvT5Q8JjksP_UJ0PgI7zRYTlVhBUZE2hBjMYak6uvwGZqiP95BYU-GiNLsvEzoVH6by0lrO5rkyEgROF4b9pyZC7X0yPH1rCE6Gq1puqBBwh46rDdK0H22mSmoup_x-wWxfz2sNcR7eKH6oNfJ6Va99lPnb-jE97Y_wW5_080v1XA3M7B2oE2PEuN5SMCSM98r3nZz_YQVu--FBb5S-vt-pZDIx5kAG5cfcC5ScJPsmkdilw74bTbRHcN4HBPWw8iN-InD6hjAfMO6aRoUqS7fdNor5U1YwPuBYrBD9Q3WCA=="
STATION_ID = "44109012"       # Identifiant de la station
DATE_DEBUT = "2022-01-01"     # Format AAAA-MM-JJ
DATE_FIN   = "2022-12-31"     # Format AAAA-MM-JJ

# ==========================================

headers = {
    'accept': '*/*',
    'apikey': API_KEY
}

# --- ÉTAPE 1 : COMMANDER LES DONNÉES ---
print("1. Lancement de la commande...")

# Le script formate automatiquement les dates pour l'API
debut_api = f"{DATE_DEBUT}T00%3A00%3A00Z"
fin_api = f"{DATE_FIN}T00%3A00%3A00Z"

# Construction dynamique de l'URL avec les variables
url_commande = f"https://public-api.meteofrance.fr/public/DPClim/v1/commande-station/quotidienne?id-station={STATION_ID}&date-deb-periode={debut_api}&date-fin-periode={fin_api}"

reponse_commande = requests.get(url_commande, headers=headers)

if reponse_commande.status_code in [200, 202]:
    data_commande = reponse_commande.json()
    numero_commande = data_commande.get('elaboreProduitAvecDemandeResponse', {}).get('return')
    print(f"-> Succès ! Numéro de commande : {numero_commande}")
else:
    print(f"Erreur lors de la commande (Code {reponse_commande.status_code})")
    print(reponse_commande.text)
    exit()

# --- PAUSE POUR LA GÉNÉRATION ---
print("2. Attente de 15 secondes pour la préparation du fichier...")
time.sleep(15)

# --- ÉTAPE 2 : TÉLÉCHARGER LE FICHIER ---
print("3. Téléchargement des données...")
url_fichier = f"https://public-api.meteofrance.fr/public/DPClim/v1/commande/fichier?id-cmde={numero_commande}"

reponse_fichier = requests.get(url_fichier, headers=headers)

if reponse_fichier.status_code in [200, 201, 202, 203]:
    # On nomme le fichier dynamiquement selon la station et les dates
    nom_du_fichier = f"meteo_{STATION_ID}_{DATE_DEBUT}_au_{DATE_FIN}.csv"
    with open(nom_du_fichier, 'wb') as fichier:
        fichier.write(reponse_fichier.content)
    print(f"-> Terminé ! Données sauvegardées dans '{nom_du_fichier}'")

elif reponse_fichier.status_code == 204:
    print("-> Le fichier n'est pas encore prêt. Relance l'étape 2 ou augmente le time.sleep().")

elif reponse_fichier.status_code == 404:
    print("-> Erreur 404 : La station ne contient pas de données pour cette période précise.")
else:
    print(f"Erreur lors du téléchargement (Code {reponse_fichier.status_code})")
    print(reponse_fichier.text)
