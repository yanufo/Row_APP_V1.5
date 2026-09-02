import streamlit as st

st.set_page_config(
    page_title="App Prototype",
    page_icon="🛩️",
    layout="wide",
)

home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
)

row_reports = st.Page(
    "pages/Row_report.py",
    title="Right-of-Way Reports",
    icon="⚡️",
)

solar_reports = st.Page(
    "pages/Solar_report.py",
    title="Solar Reports",
    icon="☀️",
)

pg = st.navigation([
    home,
    row_reports,
    solar_reports,
])

pg.run()