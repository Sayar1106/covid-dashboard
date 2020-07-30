
def fetch_url(date, country=None):
    """
    Function fetches the url of the most recent report.

    :param date: datetime object
    :param country: str
    :return: str
    """
    DATA_URL = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/"
                "csse_covid_19_daily_reports/{}.csv".format(date.date().strftime("%m-%d-%Y")))
    if country == "US":
        DATA_URL = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/"
                    "csse_covid_19_daily_reports_us/{}.csv".format(date.date().strftime("%m-%d-%Y")))

    return DATA_URL
