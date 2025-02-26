# import relevant packages
import streamlit as st
import pandas as pd
import requests
import io
import os
from dotenv import load_dotenv
from evidently_monitoring import ProjectMonitor
load_dotenv()

# Retrieve credentials from .env file
ORG_ID = os.getenv("evidently_org_id")
API_KEY = os.getenv("evidently_ai_key")
PROJECT_NAME = "DexterCyberLabTask"
# DATA_PATH = r"data\Cleaned_used_cars_data.csv"  # Path to new dataset


st.markdown(
        """
        <style>
        /* Style the sidebar */
        [data-testid="stSidebar"] {
        background-color: rgb(30, 144, 255); /* Light Blue */
            color: black; /* Text color inside the sidebar */
        }
        </style>
        """,
        unsafe_allow_html=True)


# Design main page
st.markdown(
    """
    <style>
        .header-container {
            text-align: center;
            font-family: Arial, sans-serif;
            margin-top: 50px;
        }
        .small-text {
            font-size: 1rem;
            font-weight: bold;
            display: block;
        }
        .big-text {
            font-size: 3rem;
            font-weight: bold;
            margin-top: -10px;
        }
    </style>

<div class="header-container">
    <span class="big-text">Track Your Fitness Like Never Before!</span>
    <span class="small-text">Accurately Predict the amount of calories burned</span>
</div>
    """,
    unsafe_allow_html=True)
# add spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# function to make api call for single row
def makeRequest(data):
    url = "http://127.0.0.1:3000/predStream/"

    # Convert DataFrame to JSON dictionary
    json_data = {"data": data.to_dict(orient="list")}  

    response = requests.post(url, json=json_data)
    
    # return the response
    return response.json()['prediction']

# function to make api call for batch predictions
def makeBatchRequest(dataframe):
    url = "http://127.0.0.1:3000/predBatch/"

    # Convert DataFrame to JSON dictionary
    json_data = {"data": dataframe.to_dict(orient="list")}

    # Send request to API
    response = requests.post(url, json=json_data)

    # Return the predictions
    # return response.json()
    return response.json()['prediction']

# get the data
df = pd.read_csv("data/Activity.csv")

predictionType = st.sidebar.selectbox(label="Select Prediction Type",
                                      options=['None','Single Prediction', 'Batch Prediction'])

if predictionType == 'Single Prediction':

    # design side bar
    # Creating sidebar inputs for each column to collect user inputs
    data = {
        "Total_Distance": [float(st.sidebar.text_input("Total Distance (miles)", value="0"))],
        "Tracker_Distance": [float(st.sidebar.text_input("Tracker Distance (miles)", value="0"))],
        "Logged_Activities_Distance": [float(st.sidebar.text_input("Logged Activities Distance (miles)", value="0"))],
        "Very_Active_Distance": [float(st.sidebar.text_input("Very Active Distance (miles)", value="0"))],
        "Moderately_Active_Distance": [float(st.sidebar.text_input("Moderately Active Distance (miles)", value="0"))],
        "Light_Active_Distance": [float(st.sidebar.text_input("Light Active Distance (miles)", value="0"))],
        "Sedentary_Active_Distance": [float(st.sidebar.text_input("Sedentary Active Distance (miles)", value="0"))],
        "Very_Active_Minutes": [float(st.sidebar.text_input("Very Active Minutes", value="0"))],
        "Fairly_Active_Minutes": [float(st.sidebar.text_input("Fairly Active Minutes", value="0"))],
        "Lightly_Active_Minutes": [float(st.sidebar.text_input("Lightly Active Minutes", value="0"))],
        "Sedentary_Minutes": [float(st.sidebar.text_input("Sedentary Minutes", value="0"))],
        "Steps": [int(st.sidebar.text_input("Steps Taken", value="0"))],
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # display the data dynamically
    st.dataframe(data)

    # Custom button styling for the button
    button_style = """
            <style>
            div.stButton > button {
                display: block;
                margin: 0 auto;
                font-size: 18px;
                font-weight: bold;
                background-color: rgb(30, 144, 255);
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                transition: 0.3s;
                border: none;
            }
            div.stButton > button:hover {
                background-color: rgb(82, 74, 92);
                transform: scale(1.05);
            }
            </style>
        """
    st.markdown(button_style, unsafe_allow_html=True)

    # wrap button to the endpoint
    if st.button("Get Prediction"):
        value = makeRequest(df)
        # display the prediction in desired format
        st.markdown(
            f"""
            <div style="text-align: center; font-weight: bold; font-size: 24px;">
                The estimated amount of calories burned is: {value:,.2f} Joules
            </div>
            """,
            unsafe_allow_html=True
        )
# if user wishes to do a batch prediction
if predictionType == 'Batch Prediction':
    file_uploader = st.file_uploader(
        label="Upload CSV file",
        accept_multiple_files=False,
        type=['csv']
    )

    def main(newPath):
        # Initialize the ProjectMonitor
        monitor = ProjectMonitor(PROJECT_NAME, ORG_ID, API_KEY)

        # Create a new project or retrieve an existing one
        monitor.createNewProject(description="Dexter CyberLab Task")
        
        project = monitor.getProject()
        if project == "Project not found":
            print("Project does not exist, please check your settings.")
        
        # Generate and upload the report
        report = monitor.getReport(newPath=newPath)
        # print("Report generated successfully:", report)
        return report

    
    if file_uploader:
            # Custom button styling for the button
        button_style = """
            <style>
            /* Styling for both st.button and st.download_button */
            div.stButton > button, div.stDownloadButton > button {
                display: block;
                margin: 0 auto;
                font-size: 18px;
                font-weight: bold;
                background-color: rgb(30, 144, 255);
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                transition: 0.3s;
                border: none;
            }
            div.stButton > button:hover, div.stDownloadButton > button:hover {
                background-color: rgb(82, 74, 92);
                transform: scale(1.05);
            }
            </style>
        """

        st.markdown(button_style, unsafe_allow_html=True)
        newData = pd.read_csv(file_uploader)
        # implement any initial preprocessing
        newData.drop(['UserID', 'Date'], axis=1, inplace=True)
        # save the newData for data monitoring
        newData.to_csv('data/new_data.csv', index=False)


        button = st.button("Download Batch Prediction Result")
        if button:
            predictions = makeBatchRequest(newData)
            newData['Predictions'] = predictions


            # Convert DataFrame to CSV format
            csv_data = newData.to_csv(index=False)

            # Convert string CSV data to bytes
            csv_bytes = io.BytesIO()
            csv_bytes.write(csv_data.encode())
            csv_bytes.seek(0)

            # Update the download button
            st.download_button(label='Download Batch Result', data=csv_bytes, file_name='output.csv', mime='text/csv')
        
        # st.write(file_uploader.name)
        viewReport = st.sidebar.button("Push Data Monitoring Report to Evidently Cloud")
        if viewReport:
            with st.spinner("Publishing Monitoring Report To Evidently Cloud"):
                main("data/new_data.csv")
                

    
