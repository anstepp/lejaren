import pathlib

import streamlit as st
from pages import (
    autotranscriber,
    hello_world,
    tutorial_2,
    tutorial_3,
    tutorial_4,
    tutorial_5,
)

APP_DIR = pathlib.Path(__file__).parent
IMAGE_DIR = APP_DIR / "pages" / "images"

st.set_page_config(
    page_title="lejaren: Computer-Aided Composition and musical prototpying in Python"
)

st.sidebar.header("Lejaren Examples & Tutorials")
st.sidebar.markdown(
    """`lejaren` is a Python library that enables Computer-Aided Composition and musical prototpying."""
)

lejaren_github_expander = st.sidebar.expander("lejaren on Github")
col1, col2 = lejaren_github_expander.columns([1, 6])
col1.image(str(IMAGE_DIR / "github_icon_64px.png"))
col2.markdown(f"""[anstepp/lejaren](https://github.com/anstepp/lejaren)""")

pages = {
    "AutoTranscriber Example": autotranscriber,
    "Tutorial 1: Hello, World": hello_world,
    "Tutorial 2: Major Scales": tutorial_2,
    "Tutorial 3: Major Scales, Another Way": tutorial_3,
    "Tutorial 4: Sogetto Cavato": tutorial_4,
    "Tutorial 5: More Sogetto Cavato": tutorial_5,
}

page_names = [
    "AutoTranscriber Example",
    "Tutorial 1: Hello, World",
    "Tutorial 2: Major Scales",
    "Tutorial 3: Major Scales, Another Way",
    "Tutorial 4: Sogetto Cavato",
    "Tutorial 5: More Sogetto Cavato",
]

page_selection = st.sidebar.selectbox(
    "Select example or tutorial page:", page_names, index=1
)

page = pages[page_selection]

with st.spinner(f"Loading {page_selection}..."):
    page.main()
