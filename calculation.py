import numpy as np
import os


def calcul_mehlich3(df_merge):
    calc_cols_1 = []
    calc_cols_2 = []
    for col_name in df_merge.columns:
        if (col_name == 'No. de Lab' or col_name == 'N0 échantillon' or col_name == 'Poids (g)'):
            continue
        if (col_name[0:2] == 'P ' or col_name[0:2] == 'Al' or col_name[0:2] == 'Fe'):
            calc_cols_1.append(col_name)
        else:
            calc_cols_2.append(col_name)

    def calcul_1(num):
        if num == np.nan:
            return np.nan
        calc = (num * 30)/3
        return calc

    def calcul_2(num, poids):
        if (poids == 0 or poids == np.nan or num == np.nan):
            return np.nan
        calc = (num * 30)/poids
        return calc

    for cols in calc_cols_1:
        df_merge[cols] = df_merge[cols].apply(calcul_1)

    for col in calc_cols_2:
        df_merge[col] = list(map(calcul_2, df_merge[col], df_merge['Poids (g)']))

    df_merge.to_excel('Calculs Mehlich3.xlsx')

    return df_merge



def calcul_HNO3_HCL(df_merge):
    calc_cols = df_merge.columns.tolist()[3:]

    def calcul(num, poids):
        if (poids == 0 or poids == np.nan or num == np.nan):
            return np.nan
        calc = (num * 50)/poids
        return calc
    
    for cols in calc_cols:
        df_merge[cols] = list(map(calcul, df_merge[cols], df_merge['Poids (g)']))

    df_merge.to_excel('Calculs HNO3_HCl.xlsx')

    return df_merge



def calcul_H2SO4_SeO3(df_merge):
    calc_cols = df_merge.columns.tolist()[3:]

    def calcul(num, poids):
        if (poids == 0 or poids == np.nan or num == np.nan):
            return np.nan
        calc = (num * 100)/poids
        return calc
    
    for cols in calc_cols:
        df_merge[cols] = list(map(calcul, df_merge[cols], df_merge['Poids (g)']))

    df_merge.to_excel('Calculs H2SO4_SeO3.xlsx')

    return df_merge
