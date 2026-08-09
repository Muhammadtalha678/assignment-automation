from fastapi import File,UploadFile,Depends,HTTPException,status,Form
import os
import uuid
import json
from src.models.pydantic_model import data as ChatDataModal
# this for single image
def upload_images_and_get_chat_data(
        logo_image:UploadFile = File(...), #this handle required + max 1 file upload validation
        chatData:str = Form(...)
):
    MAX_FILE_SIZE = 200 * 1024 #which is 200kb size
    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg"]
    if logo_image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error":f"Only JPG/PNG images are allowed. Invalid file: {logo_image.filename}"})  

    # size checl
    logo_image.file.seek(0,2)
    img_size = logo_image.file.tell()
    logo_image.file.seek(0)

    if img_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error":"Upload Error: Max image size is 200kb"})  

    LOGO_DIR = "assets"
    os.makedirs(LOGO_DIR,exist_ok=True)
    unique_file_name = f"{uuid.uuid4()}_{logo_image.filename}"
    logo_path = os.path.join(LOGO_DIR,unique_file_name)
    with open(logo_path,"wb") as f:
         f.write(logo_image.file.read())

    # now make data as chatdata pydantic comes as str
    try:
        # first convert str to json   
        parsed_json = json.loads(chatData)   
        # now validate data by pydantic model
        validate_data = ChatDataModal(**parsed_json)
        # now add logo_path by pydantic model
        validate_data.logo_path = logo_path
    except Exception as e:
        if os.path.exists(logo_path):
             os.remove(logo_path)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail={"error":"Invalid Form Data Structure"})  
         

    return validate_data



# this for array method 
# def upload_images(
#         logo_image:List[UploadFile] = File(...)
# ):
#     MAX_FILE_SIZE = 200 * 1024 #which is 200kb size
#     # check if logo images have one image or empty or greate than one image 
#     if not logo_image or len(logo_image) == 0:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#         detail={"error":"Logo image is required"})  
#     if  len(logo_image) > 1:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#         detail={"error":"Max 1 Logo image allowes"})  
#     # check if this images file or any other file
#     for img in logo_image:
#         if not img.content_type.startswith("image/jpg") or not img.content_type.startswith("image/png"):
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#             detail={"error":f"Only images files are allowed: Invalid file:{img.filename}"})  

#         # check img sixe is not greate than 200kb
#         img.file.seek(0,2)
#         img_size = img.file.tell()
#         img.file.seek(0)

#         if img_size > MAX_FILE_SIZE:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#             detail={"error":"Upload Error: Max image size is 200kb"})  


#     return {
#         "logo_image":logo_image
#     }