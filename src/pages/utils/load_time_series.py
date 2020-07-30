import pandas as pd
import streamlit as st


@st.cache
def load_time_series():
    """
    Function aggregates and returns a dictionary of time series data.

    :return: dict
    """
    confirmed_data = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    death_data = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
    recovered_data = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

    confirmed_data = confirmed_data.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                         var_name="Date", value_name="Confirmed")
    confirmed_data["Confirmed"] = confirmed_data["Confirmed"].fillna(0)
    confirmed_data.loc[:, "Date"] = confirmed_data["Date"].apply(lambda s: pd.to_datetime(s).date())
    death_data = death_data.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                 var_name="Date", value_name="Deaths")
    death_data["Deaths"] = death_data["Deaths"].fillna(0)
    death_data.loc[:, "Date"] = death_data["Date"].apply(lambda s: pd.to_datetime(s).date())
    recovered_data = recovered_data.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                         var_name="Date", value_name="Recovered")
    recovered_data["Recovered"] = recovered_data["Recovered"].fillna(0)
    recovered_data.loc[:, "Date"] = recovered_data["Date"].apply(lambda s: pd.to_datetime(s).date())

    return {
        "Confirmed": confirmed_data,
        "Deaths": death_data,
        "Recovered": recovered_data
    }
