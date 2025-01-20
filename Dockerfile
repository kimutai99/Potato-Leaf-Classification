# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables to prevent interactive prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

# Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application files into the container
COPY . /app/

# Expose the application port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
