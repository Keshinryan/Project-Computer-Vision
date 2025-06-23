import os
import shutil
import uuid
import requests
import subprocess
from fastapi import HTTPException
from urllib.parse import urlparse

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def is_youtube_url(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url

def download_file(url: str, is_video: bool = False) -> str:
    ext = ".mp4" if is_video else ".jpg"

    try:
        # Handle YouTube URLs
        if is_youtube_url(url):
            filename = f"{uuid.uuid4()}.mp4"
            output_path = os.path.join(UPLOAD_DIR, filename)

            result = subprocess.run([
                "yt-dlp",
                "-f", "mp4",
                "-o", output_path,
                url
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result.returncode != 0 or not os.path.exists(output_path):
                raise Exception(f"YouTube download failed: {result.stderr.decode()}")

            return output_path

        # Handle direct URLs
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()

        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
        with open(file_path, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        return file_path

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Download failed: {e}")
