import pandas as pd
import streamlit as st

@st.cache
def load_data(DATA_URL, nrows=None):
    df = pd.read_csv(DATA_URL, nrows=nrows)

    return df
