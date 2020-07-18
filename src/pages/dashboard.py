import os
import streamlit  as st
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
from src.pages.utils.fetch_url import fetch_url
from src.pages.utils.load_data import load_data
from src.pages.utils.load_css import local_css
from src.pages.utils.load_time_series import load_time_series


@st.cache
def plot_snapshot_numbers(df, colors, date, country=None):
    with st.spinner("Rendering chart..."):
        colors = px.colors.qualitative.D3
        if country:
            df = df[df["Country_Region"] == country]
        fig = px.bar(y=df[["Confirmed", "Deaths", "Recovered", "Active"]].columns.tolist(),
                     x=df[["Confirmed", "Deaths", "Recovered", "Active"]].sum().values,
                     color=df[["Confirmed", "Deaths", "Recovered", "Active"]].columns.tolist(),
                     text=df[["Confirmed", "Deaths", "Recovered", "Active"]].sum().values,
                     orientation='h',
                     color_discrete_sequence=[colors[1], colors[3], colors[2], colors[0]])
        fig.update_traces(opacity=0.7,
                          textposition="inside",
                          texttemplate='%{text:.3s}',
                          hovertemplate='Status: %{y} <br>Count: %{x:,.2f}',
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
        fig = make_subplots(2, 2, subplot_titles=["Top 10 counties by cases",
                                                  "Top 10 counties by deaths",
                                                  "Top 10 counties by recoveries",
                                                  "Top 10 countries by active cases"])
        fig.append_trace(go.Bar(x=temp["Confirmed"].nlargest(n=10),
                                y=temp["Confirmed"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}',
                                ),
                         row=1, col=1)

        fig.append_trace(go.Bar(x=temp["Deaths"].nlargest(n=10),
                                y=temp["Deaths"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}',
                                ),
                         row=2, col=1)

        fig.append_trace(go.Bar(x=temp["Recovered"].nlargest(n=10),
                                y=temp["Recovered"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}',
                                ),
                         row=1, col=2)

        fig.append_trace(go.Bar(x=temp["Active"].nlargest(n=10),
                                y=temp["Active"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}'),
                         row=2, col=2)
        fig.update_yaxes(autorange="reversed")
        fig.update_traces(
            opacity=0.7,
            marker_line_color='rgb(255, 255, 255)',
            marker_line_width=2.5
        )
        fig.update_layout(height=800,
                          width=1100,
                          showlegend=False)

    return fig


def plot_incidence_rate(df, colors, date):
    with st.spinner("Rendering chart..."):
        fig = df


@st.cache
def plot_timeline(df, feature, country=None):
    color = px.colors.qualitative.Prism
    if country:
        df = df[df["Country/Region"] == country]
    temp = df.groupby(["Date"]).agg({feature: "sum"}).reset_index()
    temp["Delta_{}".format(feature)] = temp[feature].diff()
    temp["Delta_{}".format(feature)].clip(0, inplace=True)

    fig = make_subplots(2, 1, subplot_titles=["Cumulative {}".format(feature),
                                              "Daily Delta {}".format(feature)])
    fig.add_trace(go.Scatter(
        x=temp["Date"],
        y=temp[feature],
        marker=dict(color=color[2]),
        hovertemplate='Date: %{x} <br>Count: %{y:,.2f}',
    ),
        row=1, col=1)
    fig.add_trace(go.Bar(
        x=temp["Date"],
        y=temp["Delta_{}".format(feature)],
        marker=dict(color=color[6]),
        opacity=0.7,
        hovertemplate='Date: %{x} <br>Count: %{y:,.2f}'),
        row=2, col=1)
    fig.update_layout(height=800,
                      showlegend=False)

    return fig


@st.cache
def plot_province_drilled(df, country):
    fig = make_subplots(2, 2)
    df = df[df["Country_Region"] == country]
    df = df.groupby(["Province_State"]).agg({"Confirmed": "sum",
                                              "Deaths": "sum",
                                              "Recovered": "sum",
                                              "Active": "sum"})
    fig.append_trace(go.Bar(x=df["Confirmed"].nlargest(10).index,
                            y=df["Confirmed"].nlargest(10),
                            ),
                     row=1, col=1)

    fig.append_trace(go.Bar(x=df["Deaths"].nlargest(10).index,
                            y=df["Deaths"].nlargest(10),
                            ),
                     row=2, col=1)

    fig.append_trace(go.Bar(x=df["Recovered"].nlargest(10).index,
                            y=df["Recovered"].nlargest(10),
                            ),
                     row=1, col=2)

    fig.append_trace(go.Bar(x=df["Active"].nlargest(10).index,
                            y=df["Active"].nlargest(10),
                            ),
                     row=2, col=2)

    fig.update_layout(height=800, width=800)

    return fig


@st.cache(suppress_st_warning=True)
def plot_province(df, country):
    fig = None
    df = df[df["Country_Region"] == country]
    if df["Province_State"].isnull().all():
        st.info("Sorry we do not have province/state level information for {}".format(country))
    else:
        df.rename(columns={"Lat": "lat",
                           "Long_": "lon",
                           "Admin2": "City"}, inplace=True)
        df["City"].fillna("Not Available", inplace=True)
        df.loc[:, 'Scaled Confirmed'] = df.loc[:, 'Confirmed'].apply(lambda s: np.log(s))
        df.loc[:, 'Scaled Confirmed'] = df.loc[:, 'Scaled Confirmed'].apply(
            lambda s: 0 if s == -np.inf else s)
        df["Province_State"].fillna("Not Available", inplace=True)
        temp = df[["lat", "lon"]]
        temp.dropna(inplace=True)
        with open("src/pages/utils/tokens/.mapbox_token") as tfile:
            token = tfile.read()
        fig = px.scatter_mapbox(df, lat="lat", lon="lon", zoom=3, height=600, width=800,
                                size="Scaled Confirmed",
                                color="Incidence_Rate",
                                color_continuous_scale=px.colors.sequential.Hot,
                                hover_name="Combined_Key", hover_data=["City", "Province_State", "Confirmed",
                                                                       "Deaths", "Recovered"])
        fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

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
    time_series_dict = load_time_series()
    granularity = st.sidebar.selectbox("Granularity", ["Worldwide", "Country"])
    if granularity == "Country":
        country = st.sidebar.selectbox("country", df["Country_Region"].unique())
        st.title(country)
        graph_type = st.selectbox("Choose visualization", ["Total Count",
                                                           "Timeline",
                                                           "Province/State"])
        if graph_type == "Total Count":
            fig = plot_snapshot_numbers(df, px.colors.qualitative.D3, date.date(), country)
            st.plotly_chart(fig)
        elif graph_type == "Timeline":
            slider_ph = st.empty()
            feature = st.selectbox("Select one", ["Confirmed", "Deaths", "Recovered"])
            fig = plot_timeline(time_series_dict[feature], feature, country=country)
            st.plotly_chart(fig)
        elif graph_type == "Province/State":
            fig = plot_province(df, country)
            if fig is not None:
                fig_drilled = None
                if st.checkbox("Drill down"):
                    fig_drilled = plot_province_drilled(df, country)
                st.plotly_chart(fig)
                if fig_drilled is not None:
                    st.plotly_chart(fig_drilled)
    else:
        # TODO(Sayar): Add values for deltas
        PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        local_css(PATH + "/style.css")

        st.title("Worldwide")
        st.write("\n")
        st.info("Data updated as on {}".format(date.date().strftime("%d %B, %Y")))
        graph_type = st.sidebar.selectbox("Choose visualization", ["Total Count",
                                                                   "Top affected/recovered",
                                                                   "Timeline"])
        if graph_type == "Total Count":
            st.write("\n")
            st.write("\n")
            t = "<div><span class='highlight blue'>Active:  <span class='bold'>&uarr;</span> </span> <span class='highlight orange'>Confirmed:  <span class='bold'>Name</span> </span><span class='highlight red'>Deaths:  <span class='bold'>Name</span> </span> <span class='highlight green'>Recovered:  <span class='bold'>Name</span> </span></div>"
            st.markdown(t, unsafe_allow_html=True)
            fig = plot_snapshot_numbers(df, px.colors.qualitative.D3, date.date())
            st.plotly_chart(fig)
        elif graph_type == "Top affected/recovered":
            fig = plot_top_countries(df, px.colors.qualitative.D3, date.date())
            st.plotly_chart(fig)
        elif graph_type == "Timeline":
            feature = st.selectbox("Select one", ["Confirmed", "Deaths", "Recovered"])
            fig = plot_timeline(time_series_dict[feature], feature)
            st.plotly_chart(fig)
