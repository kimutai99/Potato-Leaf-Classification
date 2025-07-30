import tensorflow as tf

# 1. Load your original model
model = tf.keras.models.load_model('model.h5')

# 2. Convert to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# 3. Apply optimizations (quantization)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# 4. Convert the model
tflite_model = converter.convert()

# 5. Save the optimized model
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

print("✅ Model converted successfully to model.tflite")