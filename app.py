from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from datetime import datetime
import logging

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Treatment suggestions dictionary
TREATMENTS = {
    'Potato___Early_blight': 'Apply fungicides containing chlorothalonil or copper-based products. Remove infected leaves.',
    'Potato___Late_blight': 'Use fungicides with mancozeb. Destroy infected plants to prevent spread.',
    'Potato___healthy': 'No treatment needed. Maintain good growing conditions.'
}

try:
    model = tf.keras.models.load_model('model.h5')
    model.make_predict_function()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise

class_names = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
IMAGE_SIZE = 256

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_path):
    try:
        img = tf.keras.preprocessing.image.load_img(
            image_path, 
            target_size=(IMAGE_SIZE, IMAGE_SIZE)
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        return img_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise

def predict(img_array):
    try:
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions)]
        confidence = round(100 * (np.max(predictions[0])), 2)
        treatment = TREATMENTS.get(predicted_class, 'Consult with agricultural expert.')
        return predicted_class, confidence, treatment
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', message='No selected file')

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                
                img_array = preprocess_image(filepath)
                predicted_class, confidence, treatment = predict(img_array)
                
                return render_template('index.html', 
                                    image_path=unique_filename,
                                    predicted_label=predicted_class,
                                    confidence=confidence,
                                    treatment=treatment)

            except Exception as e:
                logger.error(f"Error processing file: {e}")
                if os.path.exists(filepath):
                    os.remove(filepath)
                return render_template('index.html', 
                                    message=f'Error processing image: {str(e)}')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)