# #Step1 ensure foleder exists

# import os
# import shutil

# from fastapi import HTTPException,APIRouter,UploadFile,File
# from fastapi.staticfiles import StaticFiles

# import app

# router=APIRouter(tags=["Upload"])


# UPLOAD_DIR ="uploads"
# if not os.path.exists(UPLOAD_DIR):
#     os.makedirs(UPLOAD_DIR)

# #stwp2 Static file setup

# router.mount("/files",StaticFiles(directory=UPLOAD_DIR),name="files")


# #step 3 upload file api 

# @router.post('/upload')
# def Upload(file: UploadFile = File(...)):
#     filename = file.filename
#     if not filename:
#         raise HTTPException(status_code=400, detail="File not selected")
    
#     file_path = os.path.join(UPLOAD_DIR,filename)
    
#     with open(file_path,"wb") as buffer:
#         shutil.copyfileobj(file.file,buffer)
        
#     return{
#         "Message":"File upload sucessfully",
#         "filename":filename,
#         "file_url":f"http://127.0.0.1:8000/files/{filename}"
#     }
    

# #step 4 get file :

# @router.get('/files/{filename}')
# def get_file(filename:str):
#     file_path = os.path.join(UPLOAD_DIR,filename)
    
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404,detail="file not found")
    
#     return {
#         "file_url":f"http://127.0.0.1:8000/files/{filename}"
#     }