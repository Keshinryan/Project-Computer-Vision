import os
import shutil
import uuid
import requests
from fastapi import HTTPException #type: ignore
import subprocess

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

        # ✅ Optional: fix moov atom if it's a video
        if is_video:
            fixed_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_fixed.mp4")
            subprocess.run([
                "ffmpeg", "-i", file_path, "-c", "copy", "-movflags", "faststart", fixed_path
            ], check=True)
            os.remove(file_path)
            return fixed_path

        return file_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Download failed: {e}")
