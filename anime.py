import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from anime_extractor import extract_anime_titles, extract_anime_url

# anime_clean.csv
csv_file_path = 'anime_clean.csv'
# Extract anime titles using the separate module
anime_titles = extract_anime_titles(csv_file_path)
anime_urls = extract_anime_url(csv_file_path)

url = ''

def display_dt():
    # request allow you to send HTTP request
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')  # main scraping


    b = 6.39

    # Dataframe Anime list 
    df = pd.DataFrame({
        "Anime": ["a", "b", "c", "d", "e", "f"],
        "Similarity Scores (based on users)": [0.1264, 0.1244, 0.2344, 0.1944, 0.4422, 0.3012],
    })

    # Rating 1-10 score chart:    
    chart_data = pd.DataFrame({"Rating": list(range(11)), "Scores": np.random.uniform(1, 5, size=11)})


    st.title("Animatch")
    
    with st.expander("Tap to select an Animes 🌀", expanded=True):
        choice = st.selectbox("", anime_titles)
        
        # Get the corresponding URL for the selected anime
        selected_url = anime_urls[anime_titles.index(choice)]

        # Scrap from corresponded url
        # if selected_url in anime_urls:
        #     score = soup.find()
        
        # Recommend button
        is_clic = st.button("Recommends")

    if is_clic:
        st.text("Here are a few recommendations ◕⩊◕")

        st.text("")
        st.text("")

        st.dataframe(df,use_container_width=True, hide_index=True)

        st.text("")
        st.text("")

        st.header(choice)
        with st.container():
            # st.markdown("Scores:   {}".format(b,b))
            st.metric("Scores: ", b)

            st.metric("Ranked", 1200)
            
            st.metric("Popularity", 5000)

            st.write("Members: ", 1)
            ''' '''
            st.write("Favourite: ", 1)
            
        # st.bar_chart(chart_data, x="Rating", y=["Scores"], color=["#0000FF"] )
    

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