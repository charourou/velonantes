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


        return df.drop(columns = 'Date formatée')

    def drop_hours(self, df_input):
        hours_col = ['0'+str(i) for i in range(10)] + [str(i) for i in range(10,24)]
        manual_sum = df_input.loc[:,hours_col].sum(axis = 1)

        # print(manual_sum)
        return df_input.drop(columns = hours_col)



    def review_quality(self):
        """
        Returns a DataFrame with:
        with quality checked Data
            - check for failure of the sensors
            - check for obvious NaNs on key features


        """


        df = df_input.copy()
        initial_nans = df[target_col].isna().sum()

        # 1. Mise à NaN des valeurs physiquement impossibles (fusion des conditions)
        mask_aberrant = (df[target_col] < 0) | (df[target_col] > max_threshold)
        df.loc[mask_aberrant, target_col] = np.nan

        # 2. Interpolation temporelle pour combler les "trous" (NaNs)
        # Ne fonctionne correctement que si l'index est un DatetimeIndex trié
        df[target_col] = df[target_col].interpolate(method='time')

        # 3. Drop des NaNs résiduels (ex: si le tout premier jour est NaN, on ne peut pas interpoler avant)
        df = df.dropna(subset=[target_col])

        nans_fixed = initial_nans + mask_aberrant.sum() - df[target_col].isna().sum()
        print(f"Qualité : {nans_fixed} valeurs aberrantes/manquantes ont été corrigées par interpolation.")

        return df
