"""create sliders"""
import datetime
import streamlit as st

def create_slider(df, key, title):
    """create a range slider"""
    min_value  = df['date_column'].min()
    max_value  = df['date_column'].max()
    date_slider = st.sidebar.slider(
        title,
        min_value=min_value - datetime.timedelta(days=1),
        max_value=max_value + datetime.timedelta(days=1),
        value=[min_value, max_value],
        format="MM/DD/YY",
        key=key)
    return date_slider

def create_date_picker(df, key, title):
    """create a date picker"""
    min_value  = df['date_column'].min()
    max_value  = df['date_column'].max()
    date_slider = st.sidebar.date_input(
            title,
            value=(min_value, max_value),
            min_value=min_value,
            max_value=max_value,
            # format="MM.DD.YY",
            key=key
        )
    return date_slider
