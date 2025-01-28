# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables to prevent interactive prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

COPY model.h5 /app/


# Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application files into the container
COPY . /app/

# Expose the application port
EXPOSE 5000
# Base Python Image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt /app/

# Install system dependencies for TensorFlow
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Run the Flask application
CMD ["python", "app.py"]
