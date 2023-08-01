import os
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import percentileofscore
import streamlit as st

file_path = os.path.join('raw_data', 'resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv')

df=pd.read_csv(file_path)

map_df=df.groupby('Address').agg(remaining_lease= ("remaining_lease", "first"),
                        town=("town", "first"),block=("block", "first"),Latitute=("Latitude", "first"),Longitude=("Longitude", "first"),
                        Flat_level=("max_floor_lvl", "max"), price_per_sqm=('resale_price', 'sum'), total_area=('floor_area_sqm', 'sum'),).assign(price_per_sqm=lambda x: x['price_per_sqm'] / x['total_area']).drop('total_area', axis=1).reset_index()
data = map_df.copy()



def boxplot(town,flat_type,estimated_price,df):
    plt.figure(figsize=(12, 8))  # Adjust the size of the plot as needed
    custom_palette =["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    town_order_midian_price=df[df['flat_type'] == f"{flat_type}"].groupby("town")['resale_price'].median().sort_values().index
    ax = sns.boxplot(data=df[df['flat_type'] == f"{flat_type}"], x='town', y="resale_price", palette=custom_palette,order=town_order_midian_price )
    plt.title(f"Distribution of Resale Prices for {flat_type} Flats by Town", fontsize=18)
    plt.xlabel("Town", fontsize=14)
    plt.ylabel("Resale Price", fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Add a background color to the plot
    plt.gca().set_facecolor('#f5f5f5')

    # Add a margin at the top of the plot to prevent the title from being cut off
    plt.tight_layout()
    plt.axhline(y=estimated_price, color='red', linestyle='dashed', label=f'Prediction Price: $ {estimated_price}')
    plt.legend()
    # Show the plot
    st.pyplot(plt)


    percentile = round(percentileofscore(df[df['flat_type'] == f"{flat_type}"]["resale_price"], estimated_price),2)

    return f"Your estimated flat price, $ {estimated_price} is at {percentile} percentile among all the {flat_type} in Singapore"

def histogram(town,flat_type,estimated_price,df):
    plt.figure(figsize=(12, 7))
    sns.histplot(data=df[df['flat_type']==f"{flat_type}"][df['town']==f"{town}"],x="resale_price",bins=30, kde=True, color='skyblue')
    plt.axvline(x= estimated_price, color='red', linestyle='dashed', label=f'Prediction Price: $ {estimated_price}')
    plt.legend()
    plt.xlabel("Resale Price")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of Resale Prices for {flat_type} Flats in {town}")
    percentile = round(percentileofscore(df[df['flat_type']==f"{flat_type}"][df['town']==f"{town}"]["resale_price"], estimated_price),2)
    st.pyplot(plt)
    return f"Your estimated flat price, $ {estimated_price} is at {percentile} percentile among all the {flat_type} in {town}"




# data['color_scale'] = data['price_per_sqm'].apply(lambda x: [int(x)*255/(data['price_per_sqm'].max()),0, 250])
data['color_scale'] = data['price_per_sqm'].apply(lambda x: [255, int(x*255/(data['price_per_sqm'].max())), int(x*255/(data['price_per_sqm'].max())), 255] \
                                                    if x > data['price_per_sqm'].median() else [int(x*255/(data['price_per_sqm'].max())), 255, int(x*255/(data['price_per_sqm'].max())),255])
def map(data,selection=False):

    tooltip = {
        "html": "<b>{Address}</b><br />"
                "<b>Town:</b> {town}<br />"
                "<b>Block:</b> {block}<br />"
                "<b>Floor level:</b> {Flat_level}<br />"
                "<b>Remaining lease:</b> {remaining_lease}<br />"
                "<b>Price/sqm:</b> $ {price_per_sqm}",
        "style": {
            "backgroundColor": "white",
            "color": "black"
        }
    }
    INITIAL_VIEW_STATE = pdk.ViewState(
    latitude=1.295002,
    longitude=103.810635,
    zoom=11,
    max_zoom=16,
    pitch=45,
    bearing=0
    )

    scatter_layer= pdk.Layer(
    "ScatterplotLayer",
    data,
    pickable=True,
    opacity=0.5,
    stroked=True,
    filled=True,
    radius_scale=5,
    radius_min_pixels=5,
    radius_max_pixels=50,
    line_width_min_pixels=1,
    get_position=['Longitude','Latitute'],
    get_line_color=[0, 0, 0],
    get_fill_color="color_scale"
    )
    column_layer = pdk.Layer(
    "ColumnLayer",
    data,
    get_position=['Longitude','Latitute'],
    get_elevation="Flat_level",
    elevation_scale=100,
    radius=25,
    get_fill_color="color_scale",
    pickable=True,
    auto_highlight=True,
    )
    if selection:
        st.pydeck_chart(pdk.Deck(
        map_style='road',
        initial_view_state=INITIAL_VIEW_STATE,
        tooltip =tooltip ,
        layers=[column_layer, scatter_layer]
        ))
    else:
        st.pydeck_chart(pdk.Deck(
        map_style='road',
        initial_view_state=INITIAL_VIEW_STATE,
        tooltip =tooltip ,
        layers=[scatter_layer]
        ))
