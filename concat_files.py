import pandas as pd
import numpy as np


def join_files(file_poids, file_resultat_IRDA):
    df_poids = pd.read_excel(file_poids)
    df_results = pd.read_excel(file_resultat_IRDA)
    
    df_results = df_results.loc[17:]
    df_results.columns = df_results.loc[17]

    for col in df_results.columns[2:]:
        ToAppend = df_results[col][19]
        ToAppend2 = df_results[col][22]
        ToAdd = '_sol'
        if not (col == 'P' or col == 'Al' or col == 'Fe'):
            ToAppend = 'mg/kg'
        new_col = col + f" ({ToAppend}{ToAdd})" + f" // {ToAppend2}"
        df_results.rename(columns = {col: new_col}, inplace=True)
    df_results.rename(columns={"Élément: ": "N0 échantillon", np.nan: "No. de Lab"}, inplace=True)

    df_results.drop([17, 18, 19, 20, 21, 22, 23], inplace=True)
    df_results.dropna(subset=['N0 échantillon'], inplace=True)

    df_poids.columns = df_poids.loc[0]
    df_poids.drop([0], inplace=True)
    df_merge = pd.merge(df_results, df_poids, on='N0 échantillon')


