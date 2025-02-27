# dexterCyberLabTask
## Fitness Tracker Data Prediction API

## **Project Overview**
This project utilizes machine learning to predict the number of calories burned based on user activity data from a fitness tracker app. The system includes model selection and tuning using PyCaret, deployment via FastAPI, and a Streamlit-based web interface for user interaction. The application also features real-time data drift monitoring with Evidently AI and is deployed on Render with CI/CD enabled for seamless updates.

## **Table of Contents**
1. [Project Workflow](#project-workflow)
2. [How to Use](#how-to-use)
3. [API Endpoints](#api-endpoints)
4. [Web Interface](#web-interface)
5. [Data Dictionary](#data-dictionary)
6. [Deployment and CI/CD](#deployment-and-cicd)
7. [Monitoring with Evidently AI](#monitoring-with-evidently-ai)
8. [Setup Instructions](#setup-instructions)
9. [Dependencies](#dependencies)

---

## **Project Workflow**
1. **Data Exploration & Preprocessing**
   - Explored and cleaned fitness tracker data.
   - Selected key features for modeling.
2. **Model Training & Optimization**
   - Used PyCaret for model selection, hyperparameter tuning, and experimentation tracking with MLflow.
   - Finalized and registered the best model.
3. **API Development & Deployment**
   - Built a FastAPI-based REST API for batch and single inference (`api_file.py`).
   - Hosted locally (`127.0.0.1:3000`) and later deployed on Render.
4. **Web Interface for User Interaction**
   - Designed a Streamlit web app (`web_app.py`) to allow users to make predictions and download batch results.
   - Integrated data drift monitoring for each batch prediction.
5. **Monitoring with Evidently AI**
   - Implemented real-time data drift detection (`evidently_monitoring.py`).
   - Monitored model performance via Evidently Cloud.
6. **Containerization & Deployment**
   - Created a Dockerfile and pushed the project to GitHub.
   - Deployed on Render with CI/CD enabled to update deployments on push events.

---

## **How to Use**

### **1. Run API Locally**
To start the FastAPI server:
```bash
python api_file
```
You can access the API documentation at `http://127.0.0.1:3000/docs`.

### **2. Make API Requests**
- **Single Prediction (POST request)**
  ```python
  import requests
  
  url = "http://127.0.0.1:3000/predStream"
  data = {"Steps": 5000, "Total_Distance": 3.5, "Very_Active_Minutes": 20, ...}
  response = requests.post(url, json=data)
  print(response.json())
  ```
- **Batch Prediction**
  ```bash
  curl -X 'POST' \
    'http://127.0.0.1:3000/predBatch' \
    -H 'Content-Type: application/json' \
    -d @batch_data.json
  ```

### **3. Use Web Interface**
To launch the Streamlit app:
```bash
streamlit run web_app.py
```
Users can:
- Upload batch data for predictions.
- View and download batch results.
- Monitor data drift in real-time.

---

## **API Endpoints**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predStream` | POST | Predicts output for a single user input |
| `/predBatch` | POST | Processes batch predictions and returns results |

---

## **Web Interface Features**
- **Upload CSV files for batch predictions.**
- **Download processed results.**
- **Track data drift using Evidently.**
- **User-friendly interface built with Streamlit.**

---

## **Data Dictionary**
The dataset contains user activity metrics recorded by a fitness tracker app.

| Column Name | Description |
|-------------|-------------|
| UserID | Unique identifier for each user |
| Date | Date of the recorded activity |
| Steps | Number of steps taken |
| Total_Distance | Total distance covered |
| Tracker_Distance | Distance recorded by the tracker |
| Logged_Activities_Distance | Distance from manually logged activities |
| Very_Active_Distance | Distance covered during very active exercises |
| Moderately_Active_Distance | Distance covered during moderate activities |
| Light_Active_Distance | Distance covered during light activities |
| Sedentary_Active_Distance | Distance while engaged in sedentary activities |
| Very_Active_Minutes | Time spent in very active activities |
| Fairly_Active_Minutes | Time spent in fairly active activities |
| Lightly_Active_Minutes | Time spent in lightly active activities |
| Sedentary_Minutes | Time spent being sedentary |
| Calories_Burned | Estimated calories burned (TARGET)|

---

## **Deployment and CI/CD**
- **Pushed code to GitHub and connected to Render.**
- **Configured automatic deployment on new commits to the `main` branch.**
- **Built a Dockerfile for containerized deployment.**

---

## **Monitoring with Evidently AI**
- Real-time drift detection (`evidently_monitoring.py`).
- Upload reports to Evidently Cloud for visualization.
- Users can track performance drift on Evidently cloud once given permission.

---

## **Setup Instructions**
To run the project locally:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/fitness-tracker-api.git](https://github.com/james-tabansi/dexterCyberLabTask.git
   ```
2. Navigate to the project directory:
   ```bash
   cd dexterCyberLabTask
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Creat a .env file to hold key credentials (evidently_ai_key, evidently_org_id)

5. Start the FastAPI server:
   ```bash
   python api_file
   ```
6. Launch the web app:
   ```bash
   streamlit run web_app.py
   ```

---

## **Dependencies**
- **See requirements.txt file**

---

## **Contributors**
- **James Tabansi** (Project Lead)

---

