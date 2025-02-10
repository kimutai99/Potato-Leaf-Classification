# 🥔 Potato Disease Recognition App  

## Overview  
This project is a **deep learning-powered** application for detecting **potato leaf diseases**. It utilizes a **custom Convolutional Neural Network (CNN)** to classify potato leaves into different categories with **96% accuracy**.  

### Key Features:  
- 📸 **Image-based Disease Detection** – Upload a potato leaf image for real-time classification.  
- 🧠 **Deep Learning Model** – Trained on a dataset of diseased and healthy potato leaves.  
- ⚡ **High Accuracy** – Achieves **96% accuracy** on test data.  
- 🌱 **Disease Categories** – Identifies **Healthy, Early Blight,** and **Late Blight** conditions.  

This app enables early disease detection, helping farmers take preventive measures and **reduce crop losses**. 🚀  


## 🚀 Installation  

Follow these steps to set up the Potato Disease Recognition App on your local machine:  

```bash
# 1️⃣ Clone the Repository  
git clone https://github.com/kimutai99/Potato-Leaf-Classification.git
cd Potato-Leaf-Classification

# 2️⃣ Set Up a Virtual Environment (Recommended)  
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# 3️⃣ Install Dependencies  
pip install -r requirements.txt

# 4️⃣ Run the Application  
python app.py
Once the app is running, open your browser and go to http://127.0.0.1:5000/ to start using it. 🎯
```

## 🎯 How to Use 
- **Open the app**: After running the python app.py command, a local server will start, and you can access the app through your browser.
-  Build the Docker Image:
- Ensure Docker is running.
- Build the Docker imag
> docker build -t brain7854/potato-app-flask .

## To test the service locally.
### _Run the application
 - Start a container:
 > docker run -p 5000:5000 brain7854/potato-app-flask:latest

 ### _ Access the application:_
  - Open your web browser and go to: http://127.0.0.1:5000/
  
- **Upload an image**: Click on the "Upload" button and select an image of a potato leaf. The app will automatically preprocess the image and predict the disease.
  
- **View the result**: The predicted disease (Healthy, Early Blight, or Late Blight) will be displayed below the uploaded image.

## 🎯 Project Structure
    ├── app.py                     
    ├── models
    │   ├── cnn_model.keras         # Pre-trained CNN model
    │ 
    ├── data
    │   └── potato_disease.jfif     # Potato disease image c
    ├── requirements.txt            # Dependencies
    └── README.md                   # Project README
## Models
The app uses two deep learning models:
- **Custom CNN**: A Convolutional Neural Network trained on 20% of the PlantVillage dataset, specifically for potato diseases. The CNN was designed for lightweight performance while maintaining high accuracy.

## Dataset
The dataset used in this project is from the **PlantVillage** dataset, which includes thousands of images of healthy and diseased potato leaves. For this project, we focused on three classes:
- **Healthy**: No disease
- **Early Blight**: A common disease caused by the fungus *Alternaria solani*.
- **Late Blight**: A more severe disease caused by the *Phytophthora infestans* pathogen.

[Kaggle Dataset Link](https://www.kaggle.com/datasets/arjuntejaswi/plant-village)

## Evaluation
The models were evaluated using **accuracy**  metrics. The custom CNN  models achieved an accuracy score of 96%, demonstrating their effectiveness for the task of potato disease classification.

## Contact  

For any questions or feedback, feel free to reach out at:  

📧 Email: [korosbrian574@gmail.com](mailto:korosbrian574@gmail.com)  
📞 Phone: +254 768 518 488 
