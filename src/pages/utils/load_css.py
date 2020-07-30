import streamlit as st


def local_css(file_name):
    """
    Function loads the css stylesheet

    :param file_name: str
    :return: None
    """
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
