from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from HDB.logic.processor import raw_data_process,preprocessor
import pickle
import os

# Specify the path to the pickle file
pickle_file_path = os.path.join('HDB','logic', 'model_lgbm.pickle')

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
        month: str,  # 2013-07-06
        town: str,    # CHOA CHU KANG
        flat_type: str,     # 5 ROOM
        storey: str,   # 10 TO 12
        floor_area_sqm: int,    # 100
        flat_model: str,   # 'Improved'
        remaining_lease_year: int,  # 92
        remaining_lease_month: int  # 6
        ):

    data_input={'month':[pd.Timestamp(month, tz='US/Pacific')],
        'town': [town],
        'flat_type': [flat_type],
        'storey_range':[storey],
        'floor_area_sqm': [floor_area_sqm],
        'flat_model': [flat_model],
        'remaining_lease': [f'{remaining_lease_year} years {remaining_lease_month} months']}
    print("Data from user collected..................")
    data_df=pd.DataFrame(data_input)
    data_df=pd.DataFrame(data_input)
    input_feature=['month', 'town', 'flat_type', 'storey_range', 'floor_area_sqm','flat_model', 'remaining_lease']
    original_feature=['month', 'town', 'flat_type', 'block', 'street_name', 'storey_range', 'floor_area_sqm', 'flat_model', 'lease_commence_date','remaining_lease','resale_price']
    input_df=pd.DataFrame(columns=original_feature)
    for i in original_feature:
        for j in input_feature:
            if i==j:
                input_df.loc[0,i]=data_df.loc[0,j]
    input_df['month']=pd.to_datetime(input_df['month'])
    X_for_prediction,y_for_prediction=raw_data_process(input_df)
    X_processed = preprocessor(X_for_prediction)
    y_predict = model.predict(X_processed)

    return dict(Estimated_resale_price = float(y_predict))
