# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for pygame and pymunk
RUN apt-get update && apt-get install -y \
    build-essential \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev \
    python3-dev \
    python3-numpy \
    xvfb \
    freeglut3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Run a virtual framebuffer to allow pygame to work without a physical display
# This is mainly for training; evaluation will need X11 forwarding on the host
CMD ["sh", "-c", "Xvfb :99 -screen 0 800x600x24 & python train.py"]
