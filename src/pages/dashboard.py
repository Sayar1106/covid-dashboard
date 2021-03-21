import os
import streamlit as st
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
    """
    Function plots snapshots for worldwide and countries.

    :param df: DataFrame
    :param colors: list
    :param date: datetime object
    :param country: str
    :return: plotly.figure
    """
    with st.spinner("Rendering chart..."):
        colors = px.colors.qualitative.D3
        if country:
            df = df[df["Country_Region"] == country]
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df[["Confirmed", "Deaths", "Recovered", "Active"]].columns.tolist(),
                             x=df[["Confirmed", "Deaths", "Recovered", "Active"]].sum().values,
                             text=df[["Confirmed", "Deaths", "Recovered", "Active"]].sum().values,
                             orientation='h',
                             marker=dict(color=[colors[1], colors[3], colors[2], colors[0]]),
                             ),
                      )
        fig.update_traces(opacity=0.7,
                          textposition=["inside", "outside", "inside", "inside"],
                          texttemplate='%{text:.3s}',
                          hovertemplate='Status: %{y} <br>Count: %{x:,.2f}',
                          marker_line_color='rgb(255, 255, 255)',
                          marker_line_width=2.5
                          )
        fig.update_layout(
            title="Total count",
            width=800,
            legend_title_text="Status",
            xaxis=dict(title="Count"),
            yaxis=dict(showgrid=False, showticklabels=True),
        )

    return fig


@st.cache
def plot_top_countries(df, colors, date):
    """
    Function plots top countries by confirmed, deaths, recovered, active cases.

    :param df: DataFrame
    :param colors: list
    :param date: datetime object
    :return: plotly.figure
    """
    with st.spinner("Rendering chart..."):
        temp = df.groupby("Country_Region").agg({"Confirmed": "sum",
                                                 "Deaths": "sum",
                                                 "Recovered": "sum",
                                                 "Active": "sum"})
        colors = px.colors.qualitative.Prism
        fig = make_subplots(2, 2, subplot_titles=["Top 10 Countries by cases",
                                                  "Top 10 Countries by deaths",
                                                  "Top 10 Countries by recoveries",
                                                  "Top 10 Countries by active cases"])
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


@st.cache(allow_output_mutation=True)
def plot_timeline(df, feature, country=None):
    """
    Function plots  time series charts for worldwide as well as countries
    :param df: DataFrame
    :param feature: str
    :param country: str
    :return: plotly.figure, DataFrame
    """
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
        line=dict(dash="dashdot", width=4),
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
    fig.update_yaxes(showgrid=False, title="Number of cases")
    fig.update_xaxes(showgrid=False)
    fig.update_xaxes(showspikes=True, row=1, col=1)
    fig.update_yaxes(showspikes=True, row=1, col=1)
    fig.update_layout(height=800,
                      showlegend=False)

    return fig, temp


@st.cache
def plot_province_drilled(df, country):
    """
    Function computes top provinces by confirmed, deaths, recovered and active cases.

    :param df: DataFrame
    :param country: str
    :return: plotly.figure
    """
    fig = make_subplots(2, 2, subplot_titles=["Top 10 States by cases",
                                              "Top 10 States by deaths",
                                              "Top 10 States by recoveries",
                                              "Top 10 States by active cases"])
    df = df[df["Country_Region"] == country]
    df = df.groupby(["Province_State"]).agg({"Confirmed": "sum",
                                             "Deaths": "sum",
                                             "Recovered": "sum",
                                             "Active": "sum"})
    colors = px.colors.qualitative.Prism
    fig.append_trace(go.Bar(y=df["Confirmed"].nlargest(10).index,
                            x=df["Confirmed"].nlargest(10),
                            orientation='h',
                            marker=dict(color=colors),
                            hovertemplate='<br>Count: %{x:,.2f}',
                            ),
                     row=1, col=1)

    fig.append_trace(go.Bar(y=df["Deaths"].nlargest(10).index,
                            x=df["Deaths"].nlargest(10),
                            orientation='h',
                            marker=dict(color=colors),
                            hovertemplate='<br>Count: %{x:,.2f}',
                            ),
                     row=2, col=1)

    fig.append_trace(go.Bar(y=df["Recovered"].nlargest(10).index,
                            x=df["Recovered"].nlargest(10),
                            orientation='h',
                            marker=dict(color=colors),
                            hovertemplate='<br>Count: %{x:,.2f}',
                            ),
                     row=1, col=2)

    fig.append_trace(go.Bar(y=df["Active"].nlargest(10).index,
                            x=df["Active"].nlargest(10),
                            orientation='h',
                            marker=dict(color=colors),
                            hovertemplate='<br>Count: %{x:,.2f}',
                            ),
                     row=2, col=2)
    fig.update_yaxes(ticks="inside", autorange="reversed")
    fig.update_xaxes(showgrid=False)
    fig.update_traces(opacity=0.7,
                      marker_line_color='rgb(255, 255, 255)',
                      marker_line_width=2.5
                      )
    fig.update_layout(height=800, width=1200,
                      showlegend=False)

    return fig


def load_day_change(time_series_dict, keys, granularity, country=None):
    """
    Function computes the delta change in confirmed, deaths, recovered and active cases over a single day

    :param time_series_dict: dict
    :param keys: list
    :param granularity: str
    :param country: str
    :return: plotly.figure
    """
    response_dict = {}
    PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    local_css(PATH + "/style.css")
    curr = 0
    prev = 0
    for key in keys:
        if granularity == "Country":
            _, temp = plot_timeline(time_series_dict[key], key, country=country)
        else:
            _, temp = plot_timeline(time_series_dict[key], key)
        prev = temp.iloc[-2, -2]
        curr = temp.iloc[-1, -2]
        if (curr - prev) >= 0:
            arrow = "&uarr;"
        else:
            arrow = "&darr;"
        response_dict[key] = [arrow, abs(curr - prev)]

    val = response_dict["Confirmed"][1] - response_dict["Deaths"][1] - response_dict["Recovered"][1]
    if val >= 0:
        response_dict["Active"] = ["&uarr;", abs(val)]
    else:
        response_dict["Active"] = ["&darr;", abs(val)]

    st.write("\n")
    st.write("\n")
    t = (
        f"<div><span class='highlight blue'>Active:  <span class='bold'>{response_dict['Active'][0]} {response_dict['Active'][1]}</span> </span>"
        f"<span class='highlight orange'>Confirmed:  <span class='bold'>{response_dict['Confirmed'][0]} {response_dict['Confirmed'][1]}</span> </span>"
        f"<span class='highlight red'>Deaths:  <span class='bold'>{response_dict['Deaths'][0]} {response_dict['Deaths'][1]}</span> </span> "
        f"<span class='highlight green'>Recovered:  <span class='bold'>{response_dict['Deaths'][0]} {response_dict['Recovered'][1]}</span> </span></div>")

    st.markdown(t, unsafe_allow_html=True)


@st.cache(suppress_st_warning=True)
def plot_province(df, country):
    """
    Function plots the map of a country with the state/county level information as a hover.

    :param df: DataFrame
    :param country: str
    :return: plotly.figure
    """
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
                                color="Incident_Rate",
                                color_continuous_scale=px.colors.sequential.Hot,
                                hover_name="Combined_Key", hover_data=["City", "Province_State", "Confirmed",
                                                                       "Deaths", "Recovered"])
        fig.update_traces(opacity=0.7)
        fig.update_layout(mapbox_style="dark", height=1000, width=1000, mapbox_accesstoken=token)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


def main():
    pio.templates.default = "plotly_dark"
    date = datetime.today()
    df = None
    while True:
        try:
            df = load_data(fetch_url(date))
        except Exception as e:
            date = date - timedelta(days=1)
            continue
        break
    time_series_dict = load_time_series()
    granularity = st.sidebar.selectbox("Granularity", ["Worldwide", "Country"])
    if granularity == "Country":
        country = st.sidebar.selectbox("country", df["Country_Region"].unique())
        st.title(country)
        graph_type = st.selectbox("Choose visualization", ["Total Count",
                                                           "Timeline",
                                                           "Province/State"])
        if graph_type == "Total Count":
            st.subheader("One day change")
            load_day_change(time_series_dict, time_series_dict.keys(), granularity, country=country)
            fig = plot_snapshot_numbers(df, px.colors.qualitative.D3, date.date(), country)
            st.plotly_chart(fig)
        elif graph_type == "Timeline":
            feature = st.selectbox("Select one", ["Confirmed", "Deaths", "Recovered"])
            fig, _ = plot_timeline(time_series_dict[feature], feature, country=country)
            st.plotly_chart(fig)
        elif graph_type == "Province/State":
            fig = plot_province(df, country)
            if fig is not None:
                fig_drilled = None
                flag = st.checkbox("Summary (click and scroll)")
                st.subheader("Hover Map")
                st.plotly_chart(fig)
                if flag:
                    if country == "US":
                        fig_drilled = plot_province_drilled(load_data(fetch_url(date, country="US")), country)
                    else:
                        fig_drilled = plot_province_drilled(df, country)
                if fig_drilled is not None:
                    st.subheader("Summary")
                    st.plotly_chart(fig_drilled)
    else:
        # TODO(Sayar): Add values for deltas
        st.title("Worldwide")
        st.write("\n")
        st.info("Data updated as on {}".format(date.date().strftime("%d %B, %Y")))
        graph_type = st.sidebar.selectbox("Choose visualization", ["Total Count",
                                                                   "Top affected/recovered",
                                                                   "Timeline"])
        if graph_type == "Total Count":
            st.subheader("One day change")
            load_day_change(time_series_dict, time_series_dict.keys(), granularity)
            fig = plot_snapshot_numbers(df, px.colors.qualitative.D3, date.date())
            st.plotly_chart(fig)
        elif graph_type == "Top affected/recovered":
            fig = plot_top_countries(df, px.colors.qualitative.D3, date.date())
            st.plotly_chart(fig)
        elif graph_type == "Timeline":
            feature = st.selectbox("Select one", ["Confirmed", "Deaths", "Recovered"])
            fig, _ = plot_timeline(time_series_dict[feature], feature)
            st.plotly_chart(fig)
