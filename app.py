from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from datetime import datetime
import logging

app = Flask(__name__)

# ===== Configuration =====
app.config.update(
    UPLOAD_FOLDER='static/uploads',  # CHANGED from '/tmp/uploads'
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg'},
    MAX_CONTENT_LENGTH=5 * 1024 * 1024,
    MODEL_PATH="model.tflite"
)

# ===== Setup =====
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== Model Loading =====
try:
    interpreter = tf.lite.Interpreter(model_path=app.config['MODEL_PATH'])
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    MODEL_INPUT_SIZE = input_details[0]['shape'][1]
    logger.info(f"Model expects input size: {MODEL_INPUT_SIZE}x{MODEL_INPUT_SIZE}")
except Exception as e:
    logger.error(f"Model loading failed: {e}")
    raise

# ===== Routes =====
@app.route('/display/<filename>')  # NEW ROUTE ADDED
def display_image(filename):
    """Serve uploaded images"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file selected')
            
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', message='No file selected')

        if file and allowed_file(file.filename):
            try:
                # Save file
                filename = secure_filename(file.filename)
                unique_filename = f"leaf_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                
                # Process image
                img_array = preprocess_image(filepath)
                predicted_class, confidence, treatment = predict(img_array)
                
                return render_template(
                    'index.html',
                    image_path=unique_filename,  # CHANGED: Pass filename only
                    predicted_label=predicted_class,
                    confidence=confidence,
                    treatment=treatment
                )
                
            except Exception as e:
                logger.error(f"Error: {e}")
                return render_template('index.html', message=str(e))
    
    return render_template('index.html')

# ===== Helper Functions =====
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(
        image_path, 
        target_size=(MODEL_INPUT_SIZE, MODEL_INPUT_SIZE)
    )
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    return np.expand_dims(img_array, axis=0).astype(np.float32)

def predict(img_array):
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy'][np.argmax(predictions)]
    confidence = round(100 * np.max(predictions[0]), 2)
    treatment = {
        'Potato___Early_blight': 'Apply chlorothalonil fungicide',
        'Potato___Late_blight': 'Use mancozeb fungicide',
        'Potato___healthy': 'No treatment needed'
    }.get(predicted_class, 'Consult an expert')
    return predicted_class, confidence, treatment

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)