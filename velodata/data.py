from pathlib import Path
import pandas as pd


class VeloData:
    """
    The VeloData class provides methods to interact with data.nantesmetropole.fr.

    Attributes:
        base_url (str): The root URL for the API catalog.
        default_dataset (str): The default ID for the bike counting dataset.
    """

    base_url = "https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/"
    default_dataset = "244400404_comptages-velo-nantes-metropole"

    def get_data(self, dataset_id=None, url=None):
        """
        Loads and returns data from the Open Data portal as a Pandas DataFrame.

        Args:
            dataset_id (str, optional): The specific dataset ID to fetch.
            url (str, optional): A complete custom URL to bypass the builder.
        Returns:
            pd.DataFrame: The loaded data, or an empty DataFrame if it fails.
        """

        if url:
            fetch_url = url
        else:   # Construit l'URL avec l'ID fourni ou l'ID par défaut
            ds_id = dataset_id if dataset_id else self.default_dataset
            fetch_url = f"{self.base_url}{ds_id}/exports/csv?lang=fr&timezone=Europe%2FParis&use_labels=true&delimiter=%3B"

        print(f"Tentative de téléchargement depuis l'API...")

        try:    # Le séparateur standard pour l'Open Data français est le point-virgule
            df = pd.read_csv(fetch_url, sep=";")
            print(f"Succès ! {len(df)} lignes chargées.")
            return df
        except Exception as e:
            print(f"Erreur lors du téléchargement des données : {e}")
            return pd.DataFrame()

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")


    def station_count(self, df, by="passages", top_n=10):
        """
        Returns the top stations based on occurrences or total bike counts.

        Args:
            df (pd.DataFrame): The raw dataframe from get_data().
            by (str): 'records' for highest row count, 'passages' for highest bike count.
            top_n (int): The number of stations to return.

        Returns:
            pd.Series: The top stations sorted descending.
        """
        if df.empty:
            print("Erreur : Le DataFrame fourni est vide.")
            return None

        # Sécurisation : Vérifier que les colonnes attendues existent
        if 'Libellé' not in df.columns:
            print("Erreur : La colonne 'Libellé' est introuvable dans le DataFrame.")
            return None

        if by == "records":
            print(f"\n--- Top {top_n} des compteurs (par nombre de relevés) ---")
            return df['Libellé'].value_counts().head(top_n)

        elif by == "passages":
            if 'Total' not in df.columns:
                print("Erreur : La colonne 'Total' est introuvable.")
                return None
            print(f"\n--- Top {top_n} des compteurs (par total de vélos) ---")
            return df.groupby('Libellé')['Total'].sum().sort_values(ascending=False).head(top_n)

        else:
            raise ValueError("L'argument 'by' doit être 'records' ou 'passages'.")
