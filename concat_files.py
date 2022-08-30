import pandas as pd
import numpy as np


def join_files(file_poids, file_resultat_IRDA):
    df_poids = pd.read_excel(file_poids)
    df_results = pd.read_excel(file_resultat_IRDA)
    
    df_results = df_results.loc[17:]
    df_results.loc[17][0] = "No. de Lab"
    df_results.loc[17][1] = "N0 échantillon"
    df_results.columns = df_results.loc[17]

    results_col = df_results.columns.tolist()
    col_update = results_col[:2]
    for col in results_col[2:]:
        if isinstance(col, float):
            col_update.append(col)
            continue
        name = ''
        for char in col:
            if char == ' ':
                break
            name += char
        col_update.append(name)
    
    df_results.columns = col_update
    if np.nan in col_update:
        df_results.drop([np.nan], axis = 1, inplace=True)

    for col in df_results.columns[2:]:
        ToAppend = df_results[col][19]
        ToAppend2 = df_results[col][22]
        ToAdd = '_sol'
        if not (col == 'P' or col == 'Al' or col == 'Fe'):
            ToAppend = 'mg/kg'
        new_col = col + f" ({ToAppend}{ToAdd})" + f" // {ToAppend2}"
        df_results.rename(columns = {col: new_col}, inplace=True)

    df_results.drop([17, 18, 19, 20, 21, 22, 23], inplace=True)
    df_results.dropna(subset=['N0 échantillon'], inplace=True)

    df_poids.loc[0][0] = "N0 échantillon"
    df_poids.loc[0][1] = 'Poids (g)'
    df_poids.columns = df_poids.loc[0]
    df_poids.drop([0], inplace=True)
    df_results = df_results.astype({"N0 échantillon": "str"})
    df_poids = df_poids.astype({"N0 échantillon": "str"})
    df_merge = pd.merge(df_results, df_poids, on='N0 échantillon')
    cols = df_merge.columns.tolist()
    cols = cols[:2] + cols[-1:] + cols[2:-1]
    df_merge = df_merge[cols]
    df_merge = df_merge.astype({'No. de Lab': "str"})
    df_merge[cols[2:len(cols)]] = df_merge[cols[2:len(cols)]].astype('float64')

    return df_merge


