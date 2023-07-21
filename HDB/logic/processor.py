
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder,FunctionTransformer
from sklearn.compose import ColumnTransformer

def raw_data_process(df: pd.DataFrame):
    print("Raw data process in progress.....................")
    '''
    Takes in raw data (in DataFrame),
    returns X (pd.DataFrame), y (pd.Series)
    where X has unused columns removed,
    and the features are the same as the one generated from user input.
    '''
    X = df.drop(columns = ['resale_price', 'block', 'street_name', 'lease_commence_date'])
    y = df['resale_price']

    # X is left with month, town, flat_type,
    # storey_range (string), floor_area_sqm, flat_model, remaining_lease
    # To get to the same features as user input, we have to process storey_range

    X['storey'] = X['storey_range'].apply(lambda x: int(x[:2]))
    X.drop(columns = ['storey_range'], inplace = True)

    X['sale_year'] = X['month'].dt.year
    X['sale_month'] = X['month'].dt.month

    X.drop(columns = ['month'], inplace = True)

    return X, y


def preprocessor(X: pd.DataFrame):
    print("Predicted data process in progress.....................")

    '''
    Takes in DataFrame, returns processed data.
    Transforms a dataset with 7 features into a dataset with 60 features.

    Stateless operation.
    '''
    # Convert remaining_lease from the format XX years YY months to a float (years)
    X['r_lease'] = X['remaining_lease'].apply(lambda x: (int(x[:2])) if x[9:11]== '0 ' or x[9:11] == '' else (int(x[:2]) + int(x[9:11])/12))
    X.drop(columns = ['remaining_lease'], inplace = True)

    #extract year and month details from month column and drop the month column
    X['sale_month_sin'] = np.sin(2 * np.pi * X.sale_month/12)
    X['sale_month_cos'] = np.cos(2 * np.pi * X.sale_month/12)

    X.drop(columns = ['sale_month'], inplace = True)

    def create_preprocessor() -> ColumnTransformer:
        # One hot encoding for categorical features
        town_list = ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH',
        'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
        'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
        'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL',
        'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES',
        'TOA PAYOH', 'WOODLANDS', 'YISHUN']

        flat_type_list = ['2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', '1 ROOM',
            'MULTI-GENERATION']

        flat_model_list = ['Improved', 'New Generation', 'DBSS', 'Standard', 'Apartment',
            'Simplified', 'Model A', 'Premium Apartment', 'Adjoined flat',
            'Model A-Maisonette', 'Maisonette', 'Type S1', 'Type S2',
            'Model A2', 'Terrace', 'Improved-Maisonette', 'Premium Maisonette',
            'Multi Generation', 'Premium Apartment Loft', '2-room', '3Gen']

        categorical_features_names = [np.array(town_list, dtype=object),
                                    np.array(flat_type_list, dtype=object),
                                    np.array(flat_model_list, dtype=object)]

        categorical_ohe = OneHotEncoder(
            categories = categorical_features_names,
            handle_unknown = "ignore",
            sparse = False
            )

        categorical_features = ['town', 'flat_type', 'flat_model']

        # Numerical scalars

        # Floor Area min/max
        f_area_min = 0
        f_area_max = 260

        # Storey min/max
        storey_min = 1
        storey_max = 55

        # Remaining lease years min/max
        r_lease_min = 0
        r_lease_max = 99

        f_area_pipe = FunctionTransformer(lambda p: (p - f_area_min) / (f_area_max - f_area_min))
        storey_pipe = FunctionTransformer(lambda p: (p - storey_min) / (storey_max - storey_min))
        r_lease_pipe = FunctionTransformer(lambda p: (p - r_lease_min) / (r_lease_max - r_lease_min))

        # Combined preprocessor
        final_preprocessor = ColumnTransformer(
                [
                    ("f_area_scalar", f_area_pipe, ["floor_area_sqm"]),
                    ("storey_scalar", storey_pipe, ["storey"]),
                    ("r_lease_scalar", r_lease_pipe, ["r_lease"]),
                    ("categorical", categorical_ohe, categorical_features)
                ],
                n_jobs=-1,
                remainder='passthrough'
            )
        return final_preprocessor

    preprocessor = create_preprocessor()
    X_processed = preprocessor.fit_transform(X)


    return X_processed

"""This line below should be in another py file eg. fast.py
    month: str,  # 2013-07-06
    town: str,    # CHOA CHU KANG
    flat_type: str,     # 5 ROOM
    storey: str,   # 10 TO 12
    floor_area_sqm: int,    # 100
    flat_model: str,   # 'Improved'
    remaining_lease_year: int,  # 92
    remaining_lease_month: int  # 6
    """
# data_input={'month':[pd.Timestamp(month, tz='US/Pacific')],
#     'town': [town],
#     'flat_type': [flat_type],
#     'storey_range':[storey],
#     'floor_area_sqm': [floor_area_sqm],
#     'flat_model': [flat_model],
#     'remaining_lease': [f'{remaining_lease_year} years {remaining_lease_month} months']}
# data_df=pd.DataFrame(data_input)
# data_df=pd.DataFrame(data_input)
# input_feature=['month', 'town', 'flat_type', 'storey_range', 'floor_area_sqm','flat_model', 'remaining_lease']
# original_feature=['month', 'town', 'flat_type', 'block', 'street_name', 'storey_range', 'floor_area_sqm', 'flat_model', 'lease_commence_date','remaining_lease','resale_price']
# input_df=pd.DataFrame(columns=original_feature)
# for i in original_feature:
#     for j in input_feature:
#         if i==j:
#             input_df.loc[0,i]=data_df.loc[0,j]
# input_df['month']=pd.to_datetime(input_df['month'])


### This line above should be in another py file eg. fast.py
