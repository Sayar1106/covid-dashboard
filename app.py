import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


@st.cache
def load_data(DATA_URL, nrows=None):
    df = pd.read_csv(DATA_URL, nrows=nrows)

    return df


def main():
    st.title("COVID-19 Dashboard")
    date = datetime.today()
    DATA_URL = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/"
                "csse_covid_19_daily_reports/{}.csv".format(date.date().strftime("%d-%m-%Y")))
    try:
        load_data(DATA_URL)
    except:
        date = date - timedelta(days=1)

        DATA_URL = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/"
                "csse_covid_19_daily_reports/{}.csv".format(date))

    load_state = st.text('Loading data......')
    df = load_data(DATA_URL)
    load_state.text("Loading data......done!")

    if st.checkbox("Show raw data"):
        st.subheader('Raw data')
        st.write(df)


if __name__ == "__main__":
    main()