from datetime import datetime, timedelta

def fetch_url(date):
    DATA_URL = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/"
                "csse_covid_19_daily_reports/{}.csv".format(date.date().strftime("%m-%d-%Y")))

    return DATA_URL

