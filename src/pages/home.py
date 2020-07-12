import streamlit as st
from PIL import Image

def main():
    image = Image.open("assets/monalisa-4893660_640.jpg")
    st.image(image)
    st.title("COVID-19 Dashboard")
    st.write("""
    This web-application will serve to analyze, visualize, the spread of the novel Coronavirus - 2019 (COVID - 19)
    caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). It was first identified in December 2019
    in Wuhan, Hubei, China and has resulted in an ongoing pandemic.
    """)
    st.markdown("## Symptoms")
    st.markdown(("* Fever or chills\n* Cough\n"
                "* Shortness of breath or difficulty breathing\n"
                "* Fatigue\n"
                "* Muscle or body aches\n"
                "* Headache\n"
                "* Loss of taste or smell\n"
                "* Sore throat\n"
                "* Congestion or runny nose\n"
                "* Nausea or vomiting\n"
                "* Diarrhea"))
    st.markdown("## Vaccines")
    st.markdown("Track [here](https://www.raps.org/news-and-articles/news-articles/2020/3/covid-19-vaccine-tracker)")
    st.markdown("## Resources")
    st.markdown(("* [World Health Organization](https://www.who.int/maternal_child_adolescent/links/covid19-resources-and-support-for-mncah-and-ageing/en/)\n"
                 "* [Center for Disease Control](https://www.cdc.gov/coronavirus/2019-ncov/index.html)\n"
                 "* [National Institute of Health](https://www.nih.gov/coronavirus)"))

