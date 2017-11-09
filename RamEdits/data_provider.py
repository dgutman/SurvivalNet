
import numpy as np
import pandas as pd


def data_provider(data_file='./survivalData.csv'):

    data_feed = pd.read_csv(data_file, skiprows=None, header=None)

    feature_names = data_feed.loc[0, 3:]

    data_feed.columns = data_feed.iloc[0]
    data_feed = data_feed[1:]

    survival = data_feed['Survival Time']
    censored = data_feed['Censored Status']

    feature_matrix = data_feed.iloc[0:, 3:]

    return survival, censored, feature_matrix, feature_names
