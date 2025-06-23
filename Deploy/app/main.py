from fastapi import FastAPI, UploadFile, File, HTTPException #type: ignore
from fastapi.responses import JSONResponse #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from pydantic import BaseModel #type: ignore
from ultralytics import YOLO #type: ignore
from pathlib import Path 
import os
import uuid
import shutil
import subprocess
import cv2 #type: ignore
from fastapi.staticfiles import StaticFiles #type: ignore
from app.utils import download_file

UPLOAD_DIR = "app/uploads"
RESULT_DIR = "app/results"
MODEL_PATH = "app/model/best.pt"
BASE_DIR = Path(os.getcwd())

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

app = FastAPI(title="YOLOv8 Road Damage Detection")

# Mount static folder to serve results
app.mount("/results", StaticFiles(directory=RESULT_DIR, html=False), name="results")

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

def convert_to_mp4(input_path: Path) -> Path:
    output_path = input_path.with_suffix(".mp4")
    try:
        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-movflags", "faststart",
            str(output_path)
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg conversion failed: {e}")
    return output_path

def predict_and_return_url(source_path: str) -> str:
    print(f"[INFO] Predicting file: {source_path}")

    # Clear results
    shutil.rmtree("runs/detect", ignore_errors=True)

    video_ext = (".mp4", ".avi", ".mov", ".mkv")
    is_video = source_path.lower().endswith(video_ext)

    unique_id = str(uuid.uuid4())[:8]  # Unique folder name
    result_path = os.path.join("runs", "detect", unique_id)

    results = model.predict(
        source=source_path,
        save=True,
        conf=0.25,
        stream=is_video,
        project="runs/detect",
        name=unique_id,
        exist_ok=False
    )

    if is_video:
        for _ in results:
            pass
    else:
        results = list(results)

    result_dir = Path(result_path)

    if is_video:
        avi_files = list(result_dir.rglob("*.avi"))
        if not avi_files:
            raise HTTPException(status_code=500, detail="YOLO output not found (avi)")
        converted = convert_to_mp4(avi_files[0])
        final_output_path = Path(RESULT_DIR) / converted.name
        shutil.copy(converted, final_output_path)
    else:
        img_files = list(result_dir.rglob("*.jpg"))
        if not img_files:
            raise HTTPException(status_code=500, detail="YOLO output not found (jpg)")
        final_output_path = Path(RESULT_DIR) / img_files[0].name
        shutil.copy(img_files[0], final_output_path)

    return f"/results/{final_output_path.name}"

# ---------------------------- ROUTES ----------------------------

@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    try:
        ext = file.filename.split('.')[-1].lower()
        if ext not in {"jpg", "jpeg", "png"}:
            raise HTTPException(status_code=400, detail="Invalid image file type")
        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{ext}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        result_url = predict_and_return_url(file_path)
        return JSONResponse(content={"result_url": result_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/image/url")
async def predict_image_url(request: URLRequest):
    try:
        path = download_file(request.url, is_video=False)
        result_url = predict_and_return_url(path)
        return JSONResponse(content={"result_url": result_url})
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
        result_url = predict_and_return_url(file_path)
        return JSONResponse(content={"result_url": result_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/video/url")
async def predict_video_url(request: URLRequest):
    try:
        path = download_file(request.url, is_video=True)
        if not is_valid_video(path):
            raise HTTPException(status_code=400, detail="Downloaded video is invalid or unreadable.")
        result_url = predict_and_return_url(path)
        return JSONResponse(content={"result_url": result_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
