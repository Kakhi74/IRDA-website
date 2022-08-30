import pandas as pd
import os


def organisation(df_merge):
    filt = df_merge['N0 échantillon'].str.isnumeric()
    df1 = df_merge.loc[~filt]
    echantillon = {}
    for ech in df1['N0 échantillon']:
        if echantillon.get(ech[0:2]) is None:
            echantillon[ech[0:2]] = [ech]
        else:
            echantillon[ech[0:2]].append(ech)
    current_path = os.getcwd()
    dir_num = current_path.split("\\")[-1]
    for key, value in echantillon.items():
        filt = df1['N0 échantillon'].isin(value)
        df = df1.loc[filt, :]
        os.mkdir(key)
        os.chdir(key)
        previous_path = os.getcwd()
        for element in df.columns[3:]:
            os.mkdir(element[0:2])
            os.chdir(element[0:2])
            df_element = df[['N0 échantillon', element]]
            df_element.to_excel(f"{element[0:2]}.xlsx")
            #if int(dir_num) > 0:
            #    file_path = os.getcwd().split("\\")
            #    dataframes = []
            #    for x in range(int(dir_num)+1):
            #        file_path[7] = str(x)
            #        file_path_joined = "\\".join(file_path)
            #        file_path_joined += f"\\{element[0:2]}.xlsx"
            #        dataframes.append(pd.read_excel(file_path_joined))
            #    first = dataframes[0]
            #    df = ''
            #    for second in dataframes[1:]:
            #        df = pd.merge(first, second, on='N0 échantillon')
            #        first = df
            #    first.to_excel(f"{element[0:2]} UPDATED.xlsx")
            os.chdir(previous_path)
        os.chdir(current_path)
