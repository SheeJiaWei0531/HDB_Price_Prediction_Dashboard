import streamlit as st
import pandas as pd



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
storey=st.sidebar.number_input("Enter your storey")
floor_area=st.sidebar.number_input("Enter your floor area in sqm")
remaining_lease_year=st.sidebar.number_input("Enter remaining lease year")
remaining_lease_month=st.sidebar.number_input("Enter remaining lease month")

# Row A
st.markdown("### Summary")
c1,c2,c3= st.columns(3)
