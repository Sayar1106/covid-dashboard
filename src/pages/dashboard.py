import streamlit  as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
from src.pages.utils.fetch_url import fetch_url
from src.pages.utils.load_data import load_data

@st.cache
def plot_snapshot_numbers(df, colors, date):
    with st.spinner("Rendering chart..."):
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
                          hovertemplate = 'Status: %{y} <br>Count: %{x:,.2f}',
                          marker_line_color='rgb(255, 255, 255)',
                          marker_line_width=2.5
                          )
        fig.update_layout(
            title="Total count",
            width=750,
            legend=dict(title="Status"),
            xaxis=dict(title="Count"),
            yaxis=dict(title="Status", showgrid=False, showticklabels=False)
        )

    return fig

@st.cache
def plot_top_countries(df, colors, date):
    with st.spinner("Rendering chart..."):
        temp = df.groupby("Country_Region").agg({"Confirmed": "sum",
                                                 "Deaths": "sum",
                                                 "Recovered": "sum",
                                                 "Active": "sum"})
        colors = px.colors.qualitative.Pastel
        fig = make_subplots(2,2, subplot_titles=["Top 10 counties by cases",
                                                 "Top 10 counties by deaths",
                                                 "Top 10 counties by recoveries",
                                                 "Top 10 countries by active cases"])
        fig.append_trace(go.Bar(x=temp["Confirmed"].nlargest(n=10),
                                y=temp["Confirmed"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors)),
                         row=1, col=1)

        fig.append_trace(go.Bar(x=temp["Deaths"].nlargest(n=10),
                                y=temp["Deaths"].nlargest(n=10).index,
                                orientation='h'),
                        row=2, col=1)

        fig.append_trace(go.Bar(x=temp["Recovered"].nlargest(n=10),
                                y=temp["Recovered"].nlargest(n=10).index,
                                orientation='h'),
                        row=1, col=2)

        fig.append_trace(go.Bar(x=temp["Active"].nlargest(n=10),
                                y=temp["Active"].nlargest(n=10).index,
                            orientation='h'),
                            row=2, col=2)

        fig.update_layout(height=800,
                          width=1100,)

    return fig

def main():
    pio.templates.default = "plotly_dark"
    date = datetime.today()
    DATA_URL = ""
    try:
        DATA_URL = fetch_url(date)
        df = load_data(DATA_URL)
    except:
        date = date - timedelta(days=1)
        DATA_URL = fetch_url(date)
    df = load_data(DATA_URL)
    
    st.info("Data updated as on {}".format(date.date().strftime("%d %B, %Y")))
    granularity = st.sidebar.selectbox("Granularity", ["Worldwide", "Country"])
    if granularity == "Country":
        st.sidebar.selectbox("country", df["Country_Region"].unique())
    else:
        graph_type = st.sidebar.selectbox("Choose visualization", ["Total Count",
                                                                   "Top affected"])
        if graph_type == "Total Count":
            fig = plot_snapshot_numbers(df, px.colors.qualitative.D3, date.date())
            st.plotly_chart(fig)
        elif graph_type == "Top affected":
            fig = plot_top_countries(df, px.colors.qualitative.D3, date.date())
            st.plotly_chart(fig)
