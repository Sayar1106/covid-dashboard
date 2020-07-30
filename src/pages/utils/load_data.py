import pandas as pd
import streamlit as st

@st.cache
def load_data(DATA_URL, nrows=None):
    """
    Function reads data from the url and returns a dataframe

    :param DATA_URL: str
    :param nrows: int
    :return: DataFrame
    """
    df = pd.read_csv(DATA_URL, nrows=nrows)

    return df
