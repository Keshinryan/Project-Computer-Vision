# Computer Vision Project Progress Report (25%)

**Project Name**: Pendeteksi Jalanan Rusak (Road Damage Detection)  
**Student Name**: Jason Patrick  
**Course/Institution**: Computer Vision/Politeknik Caltex Riau  
**Date**: 5/1/2025  
**Progress**: 25% Complete  

## Table of Contents
- [Project Description](#project-description)
- [25% Progress Summary](#25-progress-summary)
- [Data Pipeline](#data-pipeline)
- [Model Experiments](#model-experiments)
- [Next Steps](#next-steps)

## Project Overview
A computer vision system to detect potholes in real-time using [YOLO/SSD/Faster R-CNN] for [road maintenance/driver assistance]. 

**Key Features Target**:
- Real-time detection (30+ FPS)
- Accuracy >85% on uneven roads
- Web compatibility

## 25% Progress Summary
✅ **Completed** | ⏳ **In Progress** | ❌ **Pending**

| Task                | Status | Details                          |
|---------------------|--------|----------------------------------|
| Dataset Collection  | ✅     | 500 images from [source]         |
| Annotation          | ⏳     | 300 images labeled (VGG format)  |
| Baseline Model      | ✅     | YOLOv5-nano tested (62% mAP)     |
| Preprocessing       | ⏳     | CLAHE + Gamma correction         |

## Data Pipeline
```python```
## Data Preparation
### Dataset Source
```Roboflow```
https://universe.roboflow.com/jason-workspace-krcmo/pothole-ewv2r/dataset/4
### Dataset Structure
    Pothole-Dataset/
    ├── test/         # Raw road images
    ├── train/        # Enhanced images
    ├── valid/        # Pothole annotations
    └── data.yaml

### Annotation Example
    train: ../train/images
    val: ../valid/images
    test: ../test/images
    names: ['Hump', 'crack', 'curb', 'damage', 'dash', 'distressed', 'grate', 'manhole', 'marking', 'pothole', 'utility', 'vehicle']
## Model Experiment
### Framework Model 
```YOLOv8``` **Optimal for pothole detection** due to:
| Feature               | Benefit for Pothole Detection       |
|-----------------------|-------------------------------------|
| 🚀 **High Speed**     | 30-50 FPS on mid-range GPUs (crucial for real-time road analysis) |
| 🎯 **Improved Accuracy** | 5-10% higher mAP than YOLOv5 on small objects like potholes |
| 📱 **Multiple Sizes** | Nano (for edge devices) to XLarge (for server processing) |
| 🔧 **Simplified API** | Fewer lines of code for training compared to previous versions |

## Next Step
- Data augmentation (mosaic, rotation)
- Hyperparameter tuning (optimizer, LR)
- Training Model YOLOv8