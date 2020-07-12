import streamlit as st
import pandas as pd
import src.pages.home
import src.pages.data
import src.pages.dashboard
import src.pages.contribute
import src.pages.about


PAGES = {
    "Home": src.pages.home,
    "Data": src.pages.data,
    "Dashboard": src.pages.dashboard,
    "About": src.pages.about,
    "Contribute": src.pages.contribute
}

def main():
    st.sidebar.title("Menu")
    choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
    PAGES[choice].main()
    st.sidebar.title("Contribute")
    st.sidebar.info("Feel free to contribute to this open source project. The github link can be found "
                     "[here](https://github.com/Sayar1106/covid-dashboard)")
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Sayar Banerjee. You can learn more about me at
        [sayar1106.github.io](https://sayar1106.github.io).
        """
    )

if __name__ == "__main__":
    main()