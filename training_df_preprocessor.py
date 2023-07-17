
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

X = df.drop(columns=['resale_price'])
y = df['resale_price']


def preprocessor(df):
    """
    Input df should be a pandas dataframe.
    It will return a training format dataframe.
    """
    df['storey_range_low'] = df['storey_range'].str[:2].apply(lambda x: int(x))
    df['remaining_lease_years'] = df['remaining_lease'].str[:2].apply(lambda x: int(x))
    df['remaining_lease_months'] = df['remaining_lease'].str[9:11]
    df['remaining_lease_months'] = df['remaining_lease_months'].apply(lambda x: 0 if x == '0 ' or x =='' else x)
    df['remaining_lease_months'] = df['remaining_lease_months'].apply(lambda x: int(x))
    df['remaining_lease_years'] = df['remaining_lease_years'] + df['remaining_lease_months'].apply(lambda x: x/12)
    numerical_features = ['floor_area_sqm', 'storey_range_low', 'remaining_lease_years']
    categorical_features = ['town', 'flat_type', 'flat_model']
    df=df.drop(columns=['block','street_name','lease_commence_date','storey_range','remaining_lease','remaining_lease_months'])
    min_floor_area_sqm=31
    max_floor_area_sqm=249
    min_storey_range_low=1
    max_storey_range_low=49
    min_remaining_lease_years=42.58
    max_remaining_lease_years=99
    df['floor_area_sqm']=df['floor_area_sqm'].apply(lambda x:(x-min_floor_area_sqm)/(max_floor_area_sqm))
    df['storey_range_low']=df['storey_range_low'].apply(lambda x:(x-min_storey_range_low)/(max_storey_range_low))
    df['remaining_lease_years']=df['remaining_lease_years'].apply(lambda x:(x-min_remaining_lease_years)/(max_remaining_lease_years))
    categorical_features_names=[np.array(['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH',
        'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
        'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
        'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL',
        'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES',
        'TOA PAYOH', 'WOODLANDS', 'YISHUN'], dtype=object),np.array(['1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE',
        'MULTI-GENERATION'], dtype=object),np.array(['2-room', '3Gen', 'Adjoined flat', 'Apartment', 'DBSS', 'Improved',
        'Improved-Maisonette', 'Maisonette', 'Model A',
        'Model A-Maisonette', 'Model A2', 'Multi Generation',
        'New Generation', 'Premium Apartment', 'Premium Apartment Loft',
        'Premium Maisonette', 'Simplified', 'Standard', 'Terrace',
        'Type S1', 'Type S2'], dtype=object)]
    feature_name=np.array(['town_ANG MO KIO', 'town_BEDOK', 'town_BISHAN', 'town_BUKIT BATOK', 'town_BUKIT MERAH', 'town_BUKIT PANJANG', 'town_BUKIT TIMAH',
       'town_CENTRAL AREA', 'town_CHOA CHU KANG', 'town_CLEMENTI', 'town_GEYLANG', 'town_HOUGANG', 'town_JURONG EAST',
       'town_JURONG WEST', 'town_KALLANG/WHAMPOA', 'town_MARINE PARADE', 'town_PASIR RIS', 'town_PUNGGOL', 'town_QUEENSTOWN',
       'town_SEMBAWANG', 'town_SENGKANG', 'town_SERANGOON', 'town_TAMPINES', 'town_TOA PAYOH', 'town_WOODLANDS', 'town_YISHUN',
       'flat_type_1 ROOM', 'flat_type_2 ROOM', 'flat_type_3 ROOM', 'flat_type_4 ROOM', 'flat_type_5 ROOM', 'flat_type_EXECUTIVE',
       'flat_type_MULTI-GENERATION', 'flat_model_2-room', 'flat_model_3Gen', 'flat_model_Adjoined flat',
       'flat_model_Apartment', 'flat_model_DBSS', 'flat_model_Improved', 'flat_model_Improved-Maisonette', 'flat_model_Maisonette',
       'flat_model_Model A', 'flat_model_Model A-Maisonette', 'flat_model_Model A2', 'flat_model_Multi Generation',
       'flat_model_New Generation', 'flat_model_Premium Apartment', 'flat_model_Premium Apartment Loft',
       'flat_model_Premium Maisonette', 'flat_model_Simplified', 'flat_model_Standard', 'flat_model_Terrace', 'flat_model_Type S1',
       'flat_model_Type S2'], dtype=object)
    encoder=OneHotEncoder(categories=categorical_features_names,sparse=False)
    transformed=encoder.fit_transform(df[categorical_features])
    transformed_categorical_df=pd.DataFrame(transformed, columns=feature_name)
    df=df[['month','floor_area_sqm', 'storey_range_low', 'remaining_lease_years']]
    processed_df=pd.concat([df,transformed_categorical_df],axis=1)

    return processed_df
