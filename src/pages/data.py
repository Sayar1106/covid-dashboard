import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from src.pages.utils.load_data import load_data
from src.pages.utils.fetch_url import fetch_url


def main():
    st.title("Data")
    date = datetime.today()
    DATA_URL = ""
    try:
        DATA_URL = fetch_url(date)
        df = load_data(DATA_URL)
    except:
        date = date - timedelta(days=1)
        DATA_URL = fetch_url(date)
    load_state = st.text('Loading data......')
    df = load_data(DATA_URL)
    load_state.text("Loading data......done!")

    if st.checkbox("Show raw data"):
        st.subheader('Raw data')
        st.write(df)
