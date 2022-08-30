import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from concat_files import join_files
from calculation import calcul_mehlich3, calcul_HNO3_HCL, calcul_H2SO4_SeO3
from data_organisation import organisation


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.post("/uploadfiles")
async def uploadfiles(request: Request, files: List[UploadFile] = File(description="Multiple files as UploadFile")):
    file_Poids = ''
    file_Resultat_IRDA = ''
    file1 = files[0].filename.split()
    file2 = files[1].filename.split()
    if ((file1[0] == "Poids" or file2[0] == "Poids") and (file1[0] == "Résultats_IRDA" or file2[0] == "Résultats_IRDA") and (file1[1] == file2[1])):
        file_dir = file1[1][:-5]
        absolute_path = os.getcwd()
        os.chdir('quality_control_chart')
        dir_list1 = os.listdir()
        new_dir = True
        for directory in dir_list1:
            if directory == file_dir:
                new_dir = False
                os.chdir(file_dir)
                break
        if new_dir:
            os.mkdir(file_dir)
            os.chdir(file_dir)
        dir_list2 = os.listdir()
        if len(dir_list2) == 0:
            os.mkdir('0')
            os.chdir('0')
        if len(dir_list2) > 0:
            dir_num = str(int(dir_list2[-1]) + 1)
            os.mkdir(dir_num)
            os.chdir(dir_num)
        for xlsx in files:
            with open(f"{xlsx.filename}", "wb") as buffer:
                shutil.copyfileobj(xlsx.file, buffer)
            if xlsx.filename[0] == 'P':
                file_Poids = xlsx.filename
            if xlsx.filename[0] == 'R':
                file_Resultat_IRDA = xlsx.filename

        # Working on poids and results table in pandas
        df_merge = join_files(file_poids=file_Poids, file_resultat_IRDA=file_Resultat_IRDA)

        # Calculations on pandas dataframes
        if file_dir == 'Mehlich3':
            df_calc = calcul_mehlich3(df_merge)
            organisation(df_calc)
        if file_dir == 'HNO3_HCl':
            df_calc = calcul_HNO3_HCL(df_merge)
            organisation(df_calc)
        if file_dir == 'H2SO4_SeO3':
            df_calc = calcul_H2SO4_SeO3(df_merge)
            organisation(df_calc)

        os.chdir(absolute_path)

        ###################################
        #os.chdir('quality_control_chart')
        #os.chdir(file_dir)
        #first_path = os.getcwd()
        #dataframes = []
        #for x in range(dir_num + 1):
            #os.chdir(str(x))
        return {"file_status": 'Files uploaded successfully !'}
    else:
        return {"file_status": "ERROR, please try again with the proper filename format"}



@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})