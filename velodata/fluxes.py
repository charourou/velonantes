import pandas as pd
import numpy as np
import warnings
from velodata.data import VeloData


warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)


class Flux:
    '''
    DataFrames containing all bicyles frequencies at different spot in Nantes.
    The Base DataFrame contains several locations.
    Each row is a day worth of data.

    and various properties of these  as columns
    '''
    def __init__(self):
        """Assign an attribute ".data" to all new instances of Flux"""
        print("Initialisation de l'objet Flux...")
        self.api = VeloData()
        self.data = self.api.get_data()

    def pick_station(self, station_name = '786 - 50 Otages Vers Nord'):
        """
        Performs a selection on the self.data
        by the Boucle de comptage.
        And retains only that subset.

        returns the dataframe filtered accordingly
        """
        column_name = 'Boucle de comptage'

        df_filtered = self.data[self.data[column_name] == station_name].copy()


        print(f"Station sélectionnée : {station_name} ({len(df_filtered)} jours trouvés).")
        return df_filtered


    def horodate(self, df_input):
        """
        Get the necessary time and date information
        to make a unique day index.
        """

        df = df_input.copy()


        # infer_datetime_format=True accélère grandement le processus


        df['datetime_index'] = pd.to_datetime(df['Date formatée'], utc=True, errors='coerce')
        df = df.set_index('datetime_index').sort_index()
        df = df.drop(columns = 'Date formatée')


    def review_quality(self):
        """
        Returns a DataFrame with:
        with quality checked Data
            - check for failure of the sensors
            - check for obvious NaNs on key features


        """
        pass
