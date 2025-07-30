# 🥔 Potato Disease Classifier

## 🌱 Description
The **Potato Disease Classifier** is an AI-powered web application that helps farmers and agricultural professionals quickly identify common potato leaf diseases. Using a custom **Convolutional Neural Network (CNN)** with **96% accuracy**, the system can distinguish between:

- **Healthy potato leaves**
- **Early Blight** (caused by *Alternaria solani*)
- **Late Blight** (caused by *Phytophthora infestans*)

This tool provides instant diagnosis through a user-friendly interface, enabling early disease detection and treatment to prevent crop losses. The application is **cloud-hosted on Render** for easy access and also available for local deployment.

## 🌟 Key Features
| Feature | Benefit |
|---------|---------|
| **Real-time Analysis** | Get results in under 1 second |
| **Mobile-Compatible** | Works on smartphones in the field |
| **Detailed Reports** | Includes confidence levels and treatment suggestions |
| **Easy Deployment** | Available as web service or local installation |

## 📸 Application Preview
![Potato Disease Classifier Interface](image/work%20picture.png)  
*Web interface showing disease classification results*
## 🌟 Live Demo
[![Open in Render](https://img.shields.io/badge/Render-Deployed%20App-46E3B7?style=for-the-badge&logo=render)](https://potato-leaf-classification-4.onrender.com/)



## ✨ Key Features
- ☁️ **Cloud Hosted** on Render  
- 🧠 **96% Accurate** CNN Model  
- ⚡ **Real-Time Predictions** (<1 second)  
- 📱 **Mobile-Friendly** Interface  
- 🌱 **3-Class Detection**:  
  - Healthy  
  - Early Blight  
  - Late Blight  

## 🚀 Quick Start

### 1. Try the Live Demo 👉  
[https://potato-leaf-classification-4.onrender.com/](https://potato-leaf-classification-4.onrender.com/)

### 2. Local Installation

```bash
# Clone repository
git clone https://github.com/kimutai99/Potato-Leaf-Classification.git
cd Potato-Leaf-Classification

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Access at:
http://localhost:5000
```

### 3. Docker Deployment

```bash
docker build -t potato-disease-classifier .
docker run -p 5000:5000 potato-disease-classifier
```

## 📂 Project Structure

```
Potato-Leaf-Classification/
├── app.py                 # Flask application
├── models/
│   └── potato_model.h5    # Trained CNN model
├── static/                # CSS/JS assets
├── templates/             # HTML templates
├── screenshots/           # Application visuals
│   ├── app-screenshot.png # Main interface
│   ├── healthy.png        # Healthy example
│   ├── early-blight.png   # Early blight example
│   └── late-blight.png    # Late blight example
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
└── README.md              # This documentation
```

## 📊 Model Performance

| Metric         | Score  |
|----------------|--------|
| Accuracy       | 96%    |
| Precision      | 0.95   |
| Recall         | 0.96   |
| F1-Score       | 0.95   |
| Inference Time | 0.8s   |


## 🌟 About Me

Hi there! I'm **Brian Kimutai** — a Data Scientist, Data Analyst, and Data Engineer currently freelancing on multiple data projects. I’m passionate about building smart data solutions and sharing insights that drive real impact.

---

## ☕ Stay Connected

Let's stay in touch! Feel free to connect with me on the following platforms:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/brian-kimutai-0888352b6/)  
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=google-chrome&logoColor=white)](https://kimutai99.github.io/briankimutai.github.io/)  
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kimutai99)
