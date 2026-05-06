import pandas as pd
import numpy as np
import warnings
from velodata.data import VeloData


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

    def pick_station(self, comptage_cible = '786 - 50 Otages Vers Nord'):
        """
        Performs a selection on the self.data
        by the Boucle de comptage.
        And retains only that subset.

        returns the dataframe filtered accordingly
        """
        pass


    def horodate(self):
        """
        Get the necessary time and date information
        to make a unique day index.
        """
        # df['date'] = pd.to_datetime(df['Horodate'], utc=True)   # Conversion en format temporel
        # df = df.set_index('date')                               # On met la date en index (axe X)

        pass

    def review_quality(self):
        """
        Returns a DataFrame with:
        with quality checked Data
            - check for failure of the sensors
            - check for obvious NaNs on key features


        """
        pass
