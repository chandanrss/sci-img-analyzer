from fastapi import FastAPI, File, UploadFile
import shutil
import os
from app.image_processing import process_image


# // Database setup
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)
# //end database setup

# // FastAPI setup
app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    results = process_image(file_path)

    return results
