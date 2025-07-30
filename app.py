from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from datetime import datetime
import logging

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'  # Using tmp directory for Render
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

# Load TFLite model and allocate tensors
try:
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Get model's expected input size
    MODEL_INPUT_SIZE = input_details[0]['shape'][1]  # Assuming square input
    logger.info(f"✅ TFLite model loaded successfully. Expected input size: {MODEL_INPUT_SIZE}x{MODEL_INPUT_SIZE}")
    
    # Verify model expects square input
    if input_details[0]['shape'][1] != input_details[0]['shape'][2]:
        logger.warning(f"Model expects non-square input: {input_details[0]['shape'][1:3]}")
except Exception as e:
    logger.error(f"❌ Error loading model: {e}")
    raise

class_names = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_path):
    try:
        img = tf.keras.preprocessing.image.load_img(
            image_path, 
            target_size=(MODEL_INPUT_SIZE, MODEL_INPUT_SIZE)
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Create batch dimension
        img_array = img_array.astype(np.float32)  # Ensure correct dtype
        
        # Normalize if your model expects values in a specific range
        img_array = img_array / 255.0  # Uncomment if your model expects [0,1] range
        
        return img_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise

def predict(img_array):
    try:
        # Verify input shape matches model expectations
        if img_array.shape[1:3] != (MODEL_INPUT_SIZE, MODEL_INPUT_SIZE):
            received = img_array.shape[1:3]
            raise ValueError(f"Input shape mismatch. Expected ({MODEL_INPUT_SIZE}, {MODEL_INPUT_SIZE}), got {received}")
            
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])
        
        predicted_class = class_names[np.argmax(predictions)]
        confidence = round(100 * np.max(predictions[0]), 2)
        treatment = TREATMENTS.get(predicted_class, 'Consult with agricultural expert.')
        
        return predicted_class, confidence, treatment
    except Exception as e:
        logger.error(f"Prediction error: {e}")
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
            filepath = None
            try:
                # Save uploaded file with timestamp prefix
                filename = secure_filename(file.filename)
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                
                # Process and predict
                img_array = preprocess_image(filepath)
                predicted_class, confidence, treatment = predict(img_array)
                
                return render_template('index.html', 
                                    image_path=unique_filename,
                                    predicted_label=predicted_class,
                                    confidence=confidence,
                                    treatment=treatment)

            except Exception as e:
                logger.error(f"Request processing failed: {e}")
                if filepath and os.path.exists(filepath):
                    os.remove(filepath)
                return render_template('index.html', 
                                    message=f'Error processing image: {str(e)}')
            finally:
                # Clean up uploaded file after processing
                if filepath and os.path.exists(filepath):
                    os.remove(filepath)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)