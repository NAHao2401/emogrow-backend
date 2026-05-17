import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, Request
from app.api.deps import get_current_user

router = APIRouter(prefix="/api", tags=["Upload"])

UPLOAD_DIR = "uploads/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_audio(
    request: Request,
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    # Generate unique filename
    ext = os.path.splitext(file.filename)[1]
    if not ext:
        ext = ".m4a"  # default
    
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Return full URL
    base_url = str(request.base_url).rstrip("/")
    url = f"{base_url}/uploads/audio/{unique_filename}"
    
    return {"url": url}
