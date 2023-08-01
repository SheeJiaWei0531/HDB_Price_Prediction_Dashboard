from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from HDB.logic.processor import raw_data_process,preprocessor
import pickle
import os
import datetime

# Specify the path to the pickle file
pickle_file_path = os.path.join('HDB','logic', 'model_dt.pickle')

# Open the pickle file in binary read mode ('rb')
with open(pickle_file_path, 'rb') as file:
    # Load the data from the pickle file
    model = pickle.load(file)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():

    return {'greeting': 'Hello'}

@app.get("/predict")
def predict(
        # month: str,  # 2013-07-06
        town: str,    # CHOA CHU KANG
        flat_type: str,     # 5 ROOM
        storey: int,   # 10 TO 12
        floor_area_sqm: int,    # 100
        flat_model: str,   # 'Improved'
        remaining_lease_year: int,  # 92
        remaining_lease_month: int  # 6
        ):

    today = datetime.date.today()
    data_input = {
        'sale_year': [today.year],
        'sale_month': [today.month],
        'town': [town],
        'flat_type': [flat_type],
        'storey': [storey],
        'floor_area_sqm': [floor_area_sqm],
        'flat_model': [flat_model],
        'remaining_lease': [f'{remaining_lease_year} years {remaining_lease_month} months']
        }

    print("Loading input data.....................")
    data_df = pd.DataFrame(data_input)

    X_processed = preprocessor(data_df)

    print("Predicting user input.....................")
    y_predict = model.predict(X_processed)

    return dict(Estimated_resale_price = float(y_predict))
