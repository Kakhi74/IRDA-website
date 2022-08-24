import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import os

app = FastAPI()


def initializing_dir(dirname):
    pass



@app.post("/uploadfiles")
async def root(files: List[UploadFile] = File(description="Multiple files as UploadFile")):
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
            

        os.chdir(absolute_path)
        return {"file_status": 'Files uploaded successfully !'}
    else:
        return {"file_status": "ERROR, please try again with the proper filename format"}


@app.get("/")
async def main():
    content = """
<body>
Please insert "Poids [directory].xlsx"    &    "Résultats_IRDA [directory].xlsx"
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)