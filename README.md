# 🚧 Road Damage Detection using YOLOv8 

## Table of Contents
- [Project Overview](#project-overview)
- [Progress Summary](#progress-summary)
- [Dataset](#dataset)
- [Model](#model)
- [Instalation](#instalation)
- [Next Steps](#next-steps)

## 📌 Project Overview

This project aims to build a real-time road damage detection system for:
- **Potholes**
- **Cracks**
- **Patched Roads**


## Progress Summary
✅ **Completed** | ⏳ **In Progress** | ❌ **Pending**

| Task                | Status | Details                          |
|---------------------|--------|----------------------------------|
| Dataset Collection  | ✅     | 4000+ images from [click here](https://universe.roboflow.com/jason-workspace-krcmo/pothole-ewv2r/dataset/4)        |
| Annotation          | ✅     | 4000+ images labeled (YOLOv8 PyTorch TXT)  |
| Baseline Model      | ✅     | YOLOv8    |
| Evaluate Model      | ✅     | mAP50:    mAP50-95:  |
| Optimize hyperparameter | ✅ | optimize the pixel size, and get more data, also add more epoch to be 100 | 
| Deploy Model | ❌ | Still try to rebuilt the docker| 

### 🎯 Goals
- Accuracy > 70% on detecting pothole
- Web compatibility

## 🗂️ Dataset

📦 Source: [Roboflow Datasets](https://universe.roboflow.com/jason-workspace-krcmo/pothole_detection-hfnqo-xmx8j)  
📐 Format: YOLOv8  
📊 Size: ~4000+ annotated images

```bash
dataset/
├── train/
│   ├── images/
│   └── labels/
├── valid/
├── test/
└── data.yaml
```

---


## 🤖 Model
### 🖥️ Pipeline
- **Python**

### ⚙️ Framework
- **YOLOv8** (Ultralytics)

### 🧪 Training Details
- Epochs: 100
- Image Size: 640x640
- Device: GTX 1650 (4GB)
- Classes: `crack`, `pothole`, `patch`

### 📈 Results (Latest mAP)

| Class      | mAP@50 | mAP@50–95 |
|------------|--------|-----------|
| All        | 0.635  | 0.382     |
| Crack      | 0.452  | 0.207     |
| Patch      | 0.709  | 0.477     |
| Pothole    | 0.744  | 0.463     |

---

## 🧰 Installation

### ⚙️ Requirements
- Python ≥ 3.10.14
- PyTorch ≥ 2.0.1+cu117
- Ultralytics
- roboflow
- using GPU Nvidia GTX with 11.7

### 🔧 Setup
```bash
# Clone this repo
git clone 
cd pothole_detection-3

# Train
yolo detect train data=dataset/data.yaml model=yolov8s.pt imgsz=640 epochs=100
```

---
## 🛠️ Inference Example

```bash
yolo detect predict model=runs/detect/train/weights/best.pt source=your_video.mp4
```

---

## Deploy 
The model deployed with This FastAPI application allows you to upload or link images and videos for road damage detection using a trained YOLOv8 model.

#### Endpoints
- `POST /predict/image`: Upload image file
- `POST /predict/image/url`: Provide image URL
- `POST /predict/video`: Upload video file
- `POST /predict/video/url`: Provide video URL

#### Setup Instructions
1. Clone this repo
2. Put your `best.pt` model file in the root folder
3. Build the Docker image:
   ```bash
   docker build -t yolov8-fastapi:latest .
   ```
4. Run the container (for development):
   ```bash
   docker run --gpus all -it --rm -p 8000:8000 yolov8-fastapi
   ```
5.Run the container (for deployment):
   ```bash
   docker run --gpus all -d --name yolov8-app -p 8000:8000 yolov8-fastapi
   ```

#### Example Test
Use `curl` or Postman:
```bash
curl -X POST "http://localhost:8000/predict/image/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/image.jpg"}' --output result.jpg
```

## 🎥 Detection Demo
### 🖼️ Image Prediction Demo
![Preview](demo.jpeg)
### 🎞️Video Prediction Demo
![Video Frame](demo.gif)

## 🔜 Next Steps

✅ Data collection and annotation  
✅ Train YOLOv8 with OBB  
✅ Evaluate mAP  
✅ Optimize with hyperparameter tuning  
☐ Deploy to web

## 📎 Links

- 🔗 Dataset: [Roboflow](https://universe.roboflow.com/jason-workspace-krcmo/pothole-ewv2r/dataset/4)  

---


## 🙋‍♂️ Author

Jason Patrick  
Computer Vision – Politeknik Caltex Riau

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
