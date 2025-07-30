# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    FLASK_ENV=production

# Set the working directory
WORKDIR /app

# Install system dependencies (required for TensorFlow, OpenCV, etc.)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (to leverage Docker cache)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Create the uploads directory
RUN mkdir -p /app/static/uploads

# Expose the Flask port
EXPOSE 5000

# Run the Flask application (use Gunicorn for production)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]