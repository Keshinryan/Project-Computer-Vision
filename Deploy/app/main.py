from fastapi import FastAPI, UploadFile, File, HTTPException #type: ignore
from fastapi.responses import FileResponse #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from pydantic import BaseModel #type: ignore
from ultralytics import YOLO #type: ignore
from pathlib import Path #type: ignore
import os
import uuid
import shutil
import cv2 #type: ignore

from app.utils import download_file

UPLOAD_DIR = "app/uploads"
RESULT_DIR = "app/results"
MODEL_PATH = "app/model/best.pt"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

app = FastAPI(title="YOLOv8 Road Damage Detection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

model = YOLO(MODEL_PATH)

class URLRequest(BaseModel):
    url: str

def is_valid_video(filepath: str) -> bool:
    cap = cv2.VideoCapture(filepath)
    valid = cap.isOpened()
    cap.release()
    return valid

def predict_and_return_path(source_path: str) -> str:
    print(f"[INFO] Predicting file: {source_path}")

    # Clear old results
    for f in Path(RESULT_DIR).glob("*"):
        f.unlink()

    results = model.predict(source=source_path, save=True, conf=0.25)

    if not results or not hasattr(results[0], "save_dir"):
        raise HTTPException(status_code=500, detail="Prediction failed or no result directory created.")

    result_dir = Path(results[0].save_dir)
    print(f"[INFO] Result saved at: {result_dir}")

    predicted_files = list(result_dir.rglob("*.jpg")) + list(result_dir.rglob("*.mp4"))

    if not predicted_files:
        raise HTTPException(status_code=500, detail="No prediction output found (jpg/mp4).")

    result_path = predicted_files[0]
    final_output_path = Path(RESULT_DIR) / result_path.name
    shutil.copy(result_path, final_output_path)

    return str(final_output_path)

@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    try:
        ext = file.filename.split('.')[-1].lower()
        if ext not in {"jpg", "jpeg", "png"}:
            raise HTTPException(status_code=400, detail="Invalid image file type")
        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{ext}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        result = predict_and_return_path(file_path)
        return FileResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/image/url")
async def predict_image_url(request: URLRequest):
    try:
        path = download_file(request.url, is_video=False)
        result = predict_and_return_path(path)
        return FileResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/video")
async def predict_video(file: UploadFile = File(...)):
    try:
        ext = file.filename.split('.')[-1].lower()
        if ext not in {"mp4", "mov", "avi", "mkv"}:
            raise HTTPException(status_code=400, detail="Invalid video file type")
        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{ext}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        if not is_valid_video(file_path):
            raise HTTPException(status_code=400, detail="Uploaded video file is not valid or corrupted.")
        result = predict_and_return_path(file_path)
        return FileResponse(result, media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/video/url")
async def predict_video_url(request: URLRequest):
    try:
        path = download_file(request.url, is_video=True)
        if not is_valid_video(path):
            raise HTTPException(status_code=400, detail="Downloaded video is invalid or unreadable.")
        result = predict_and_return_path(path)
        return FileResponse(result, media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
