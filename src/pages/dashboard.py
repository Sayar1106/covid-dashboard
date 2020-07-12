import streamlit  as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
from src.pages.utils.fetch_url import fetch_url
from src.pages.utils.load_data import load_data


def plot_snapshot_numbers(df, colors, date):
    st.spinner("Rendering chart...")
    colors = px.colors.qualitative.D3
    fig = px.bar(y=df[["Confirmed", "Deaths", "Recovered", "Active"]].columns.tolist(),
                 x=df[["Confirmed", "Deaths", "Recovered", "Active"]].sum().values,
                 color=df[["Confirmed", "Deaths", "Recovered", "Active"]].columns.tolist(),
                 text=df[["Confirmed", "Deaths", "Recovered", "Active"]].sum().values,
                 orientation='h',
                 color_discrete_sequence=[colors[1], colors[3], colors[2], colors[0]])
    fig.update_traces(opacity=0.7,
                      textposition="inside",
                      texttemplate='%{text:.3s}',
                      hovertemplate = 'Status: %{y} <br>Count: %{x:,.2f}'
                      )
    fig.update_layout(
        title="Total count as on {}".format(date),
        width=750,
        legend=dict(title="Status"),
        xaxis=dict(title="Count", showgrid=False),
        yaxis=dict(title="Status", showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig)


def main():
    date = datetime.today()
    DATA_URL = ""
    try:
        DATA_URL = fetch_url(date)
        df = load_data(DATA_URL)
    except:
        date = date - timedelta(days=1)
        DATA_URL = fetch_url(date)
    df = load_data(DATA_URL)
    st.sidebar.markdown("## Country")
    plot_snapshot_numbers(df, px.colors.qualitative.D3, date.date())
    st.sidebar.selectbox("", df["Country_Region"].unique())
