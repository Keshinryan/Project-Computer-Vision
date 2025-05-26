# Computer Vision Project Progress Report (25%)

**Project Name**: Pendeteksi Kerusakan Jalan (Road Damage Detection)  
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
A computer vision system to detect potholes and other road damage in real-time using YOLO for road maintenance. 

**Key Features Target**:
- Accuracy > 70% on detecting pothole
- Web compatibility

## 25% Progress Summary
✅ **Completed** | ⏳ **In Progress** | ❌ **Pending**

| Task                | Status | Details                          |
|---------------------|--------|----------------------------------|
| Dataset Collection  | ✅     | 1000+ images from [click here](https://universe.roboflow.com/jason-workspace-krcmo/pothole-ewv2r/dataset/4)        |
| Annotation          | ✅     | 1000+ images labeled (YOLOv8 PyTorch TXT)  |
| Baseline Model      | ✅     | YOLOv8    |

## Data Pipeline
```python```
## Data Preparation
### Dataset Source
```Roboflow```
[click here](https://universe.roboflow.com/jason-workspace-krcmo/pothole-ewv2r/dataset/4)
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
    names: ['crack','manhole','pothole']
## Model Experiment
### Framework Model 
```YOLOv8``` **Optimal for pothole detection** due to:
| Feature               | Benefit for Pothole Detection       |
|-----------------------|-------------------------------------|
| 🚀 **High Speed**     | 30-50 FPS on mid-range GPUs (crucial for real-time road analysis) |
| 🎯 **Improved Accuracy** | 5-10% higher mAP than YOLOv5 on small objects like potholes |
| 📱 **Multiple Sizes** | Nano (for edge devices) to XLarge (for server processing) |
| 🔧 **Simplified API** | Fewer lines of code for training compared to previous versions |

### Model Train 
#### roboflow
[click here](https://universe.roboflow.com/jason-workspace-krcmo/pothole-ewv2r/model/2)
#### google colab
[click here](https://colab.research.google.com/drive/13OujGUSG246OVYmOJ3ZZ18A03ws-qOVe?usp=sharing)
## Next Step
- Data augmentation (mosaic, rotation, ETC)
- Hyperparameter tuning (optimizer, LR)
- Training Model YOLOv8
