from fastapi import FastAPI
import uvicorn
import pandas as pd
from pycaret.classification import load_model

# Load the saved PyCaret model
model = load_model("best_model")

# Initialize FastAPI app
app = FastAPI()

# Define a request body schema
from pydantic import BaseModel, Field
from typing import Optional, List, Dict


# class InputData(BaseModel):
#     Total_Distance: int
#     Tracker_Distance: int
#     Logged_Activities_Distance: int
#     Very_Active_Distance: int
#     Moderately_Active_Distance: int
#     Light_Active_Distance: int
#     Sedentary_Active_Distance: int
#     Very_Active_Minutes: int
#     Fairly_Active_Minutes: int
#     Lightly_Active_Minutes: int
#     Sedentary_Minutes: int
#     Steps: int
#     Calories_Burned: int


#     class Config:
#         allow_population_by_field_name = True
    
# Define prediction endpoint

# Define request body schema for `/predStream`
class NewInputData(BaseModel):
    data: Dict[str, List]

@app.post("/predStream/")
def predictFromStreamlit(payload: NewInputData):
    try:
        # Convert JSON back into a DataFrame
        df = pd.DataFrame.from_dict(payload.data)

        # Make prediction
        prediction = model.predict(df)

        return {"prediction": prediction.tolist()[0]}

    except Exception as e:
        return {"error": str(e)}
    
@app.post("/predBatch/")
def batchPredict(payload: NewInputData):
    try:
        # Convert JSON back into a DataFrame
        df = pd.DataFrame.from_dict(payload.data)

        # Make prediction
        prediction = model.predict(df)

        return {"prediction": prediction.tolist()}

    except Exception as e:
        return {"error": str(e)}
    

# Run the API locally
if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=3000)
