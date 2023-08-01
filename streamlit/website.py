import streamlit as st
import pandas as pd
from util import boxplot,histogram,map
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import percentileofscore
import os
import pydeck as pdk
import requests


st.set_page_config(layout='wide', initial_sidebar_state="expanded")

st.title('HDB Prediction And Analysis')

st.sidebar.header("Prediction input")

town=st.sidebar.selectbox("Town",('ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
        'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST', 'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL',
        'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN'))
flat_type=st.sidebar.selectbox("Flat type",('2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', '1 ROOM','MULTI-GENERATION'))
model_type=st.sidebar.selectbox("Model type",('Improved', 'New Generation', 'DBSS', 'Standard', 'Apartment',
            'Simplified', 'Model A', 'Premium Apartment', 'Adjoined flat', 'Model A-Maisonette', 'Maisonette', 'Type S1', 'Type S2',
            'Model A2', 'Terrace', 'Improved-Maisonette', 'Premium Maisonette', 'Multi Generation', 'Premium Apartment Loft', '2-room', '3Gen'))
storey=st.sidebar.number_input("Enter your storey",step=1, value=1,min_value = 1, max_value = 55)
floor_area=st.sidebar.number_input("Enter your floor area in sqm",step=1, value= 1,min_value = 1, max_value = 260)
remaining_lease_year=st.sidebar.number_input("Enter remaining lease year",step=1, value= 95,min_value = 0, max_value = 99)
remaining_lease_month=st.sidebar.number_input("Enter remaining lease month",step=1, value= 1,min_value = 0, max_value = 11)
predic_button = st.sidebar.button("Predict")


params={"town" : town,
        "flat_type" : flat_type,
        "storey" : storey,
        "floor_area_sqm" : floor_area,
        "flat_model" : model_type,
        "remaining_lease_year": remaining_lease_year,
        "remaining_lease_month" : remaining_lease_month}

url= "https://hdb-prediction-4612fd06bd0d.herokuapp.com/predict"

request = requests.get(url, params=params).json()





if "load_state" not in st.session_state:
    st.session_state.load_state=False
if predic_button or st.session_state.load_state:
    st.session_state.load_state= True



    estimated_price= round(request['Estimated_resale_price'])

    st.header(f'Based on your given input, the estimated price for your flat is $ {estimated_price}.')

    # Row A
    st.markdown("### Analysis based on transaction since year 2017 till July 2023")

    data_year= st.checkbox("Latest two years")
    c1,c2= st.columns(2)
    @st.cache_data()
    def load_data(filepath):
        return pd.read_csv(filepath)
    file_path = os.path.join('raw_data', 'resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')
    df=load_data(file_path)
    with c1:
        result_box = boxplot(town, flat_type, estimated_price,df)
        st.write(result_box)
    with c2:
        result_hist = histogram(town, flat_type, estimated_price,df)
        st.write(result_hist)


    # st.header("Analysis based on transaction since year 2021 till July 2023")

    if "load_state" not in st.session_state:
        st.session_state.load_state=False
    if data_year or st.session_state.load_state:
        st.session_state.load_state= True



        if data_year:
            st.header("Analysis based on transaction since year 2021 till July 2023")
            c3,c4= st.columns(2)
            @st.cache_data()
            def load_data(filepath):
                return pd.read_csv(filepath)
            file_path = os.path.join('../','raw_data', 'resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')
            df=load_data(file_path)
            df=df[df["year"]>=2021]

            with c3:
                result_box = boxplot(town, flat_type, estimated_price,df)
                st.write(result_box)
            with c4:
                result_hist = histogram(town, flat_type, estimated_price,df)
                st.write(result_hist)







        st.header("Interactive map based on price/sqm ")

        selection= st.checkbox("HDB")
        @st.cache_data()
        def load_data(filepath):
            return pd.read_csv(filepath)
        file_path = os.path.join('../','raw_data', 'resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')
        df=load_data(file_path)

        map_df=df.groupby('Address').agg(remaining_lease= ("remaining_lease", "first"),town=("town", "first"),block=("block", "first"),Latitute=("Latitude", "first"),
                                    Longitude=("Longitude", "first"),Flat_level=("max_floor_lvl", "max"),
                                    price_per_sqm=('resale_price', 'sum'), total_area=('floor_area_sqm', 'sum'),).assign(price_per_sqm=lambda x: x['price_per_sqm'] / x['total_area']).drop('total_area', axis=1).reset_index()

        data=map_df.copy()
        # data['color_scale'] = data['price_per_sqm'].apply(lambda x: [int(x)*255/(data['price_per_sqm'].max()),0, 230])
        data['color_scale'] = data['price_per_sqm'].apply(lambda x: [255, int(x*255/(data['price_per_sqm'].max())), int(x*255/(data['price_per_sqm'].max())), 255] \
                                                          if x > data['price_per_sqm'].median() else [int(x*255/(data['price_per_sqm'].max())), 255, int(x*255/(data['price_per_sqm'].max())),255])


        if "load_state" not in st.session_state:
            st.session_state.load_state=False
        if selection or st.session_state.load_state:
            st.session_state.load_state= True

            if selection:

                st.write(map(data, selection=True))
            else:
                st.write(map(data, selection=False))

            st.write(":red[Red color indicates price higher than the median price]")
            st.write(":green[Green color indicates price lower than the median price]")
