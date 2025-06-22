from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ultralytics import YOLO
from pathlib import Path
import os
import uuid
import shutil

from app.utils import download_file  # make sure this util is implemented correctly

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

# Load model once on startup
model = YOLO(MODEL_PATH)

class URLRequest(BaseModel):
    url: str

def predict_and_return_path(source_path: str) -> str:
    # Clear old results before prediction
    for f in Path(RESULT_DIR).glob("*"):
        f.unlink()
    # Run prediction, save results to RESULT_DIR
    model.predict(source=source_path, save=True, save_dir=RESULT_DIR, conf=0.25)
    # Return first result file path (jpg or mp4)
    results = list(Path(RESULT_DIR).rglob("*.jpg")) + list(Path(RESULT_DIR).rglob("*.mp4"))
    if not results:
        raise HTTPException(status_code=500, detail="No prediction result found.")
    return str(results[0])

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
        result = predict_and_return_path(file_path)
        return FileResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/video/url")
async def predict_video_url(request: URLRequest):
    try:
        path = download_file(request.url, is_video=True)
        result = predict_and_return_path(path)
        return FileResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))