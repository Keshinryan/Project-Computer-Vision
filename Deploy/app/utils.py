import os
import shutil
import uuid
import requests
from fastapi import HTTPException #type: ignore

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def download_file(url: str, is_video: bool = False) -> str:
    ext = ".mp4" if is_video else ".jpg"
    try:
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()

        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
        with open(file_path, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        return file_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Download failed: {e}")
