FROM nvidia/cuda:11.7.1-runtime-ubuntu20.04

# Set working directory
WORKDIR /app

# Install Python 3.10 + pip + system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common curl ffmpeg unzip libgl1 libglib2.0-0 && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y python3.10 python3.10-distutils && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    ln -s /usr/bin/python3.10 /usr/bin/python && \
    ln -s /usr/local/bin/pip /usr/bin/pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

# Copy requirements.txt
COPY requirements.txt .

# Uninstall existing torch packages (if any) just to be safe
RUN pip uninstall -y torch torchvision torchaudio || true

# Install PyTorch 2.0.1 with CUDA 11.7 explicitly
RUN pip install torch==2.0.1+cu117 torchvision==0.15.2+cu117 torchaudio==2.0.2 --extra-index-url https://download.pytorch.org/whl/cu117

# Install other Python dependencies from requirements.txt (make sure torch is NOT listed there)
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY app ./app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Start FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# for Deployment in hf or production.
# FROM python:3.10-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY app ./app

# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

