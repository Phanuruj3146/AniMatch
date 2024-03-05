import streamlit as st
import pandas as pd
import numpy as np

mood_selc = open('categorymd')  # opening mood select file
mooods = list(mood_selc)  # turn them into a list to loop through

def display_dt():

    # Dataframe Anime list 
    df = pd.DataFrame({
        "Anime": ["a", "b", "c", "d", "e", "f"],
        "Similarity Scores (based on users)": [0.1264, 0.1244, 0.2344, 0.1944, 0.4422, 0.3012],
    })

    # Rating 1-10 score chart:    
    chart_data = pd.DataFrame({"Rating": list(range(11)), "Scores": np.random.uniform(1, 5, size=11)})


    st.title("Animatch")
    
    with st.expander("Tap to select an Animes 🌀", expanded=True):
        choice = st.selectbox("", mooods)
        is_clic = st.button("Recommends")

    if is_clic:
        st.text("Here are a few recommendations ◕⩊◕")

        st.text("")
        st.text("")

        st.dataframe(df,use_container_width=True, hide_index=True)

        st.text("")
        st.text("")

        st.subheader("JJK")
        st.bar_chart(chart_data, x="Rating", y=["Scores"], color=["#0000FF"] )
    
    st.markdown(
        """
        <style>
        .streamlit-expanderHeader p {
            font-sze: 33rem;
        }
        .stSelectbox [data-testid='stMarkdownContainer'] {
            font-sze: 6rem;
        }
        .stSelectbox div[data-baseweb="select"] > div:first-child {
            border-color: #2d408d;
        }
        .stHeadingContainer [data-testid='stHeading'] {
            text-align: center;
        }
        .appview-container {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

with st.container():
    display_dt()