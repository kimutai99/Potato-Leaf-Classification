FROM tensorflow/tensorflow:latest
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt  
EXPOSE 5000
CMD ["python","flask_app.py"]  