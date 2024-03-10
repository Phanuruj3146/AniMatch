import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from anime_extractor import extract_anime_titles, extract_anime_url

# anime_clean.csv
csv_file_path = 'anime_clean.csv'
# Extract anime titles using the separate module
anime_titles = extract_anime_titles(csv_file_path)
anime_urls = extract_anime_url(csv_file_path)


def display_dt():

    url = ''
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
        if selected_url in anime_urls:
            url += selected_url
            st.write(url)
        
            # request allow you to send HTTP request
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')  # main scraping

            # Elements to display under anime statistics
            score = soup.find('span', class_="score-label").text

            image = soup.find('img', class_='lazyloaded')
            
            
            # ranked = soup.find('div', attrs={'class': 'spaceit_pad po-r js-statistics-info di-ib', 'data-id': "info2"}).text
            # ranked_str = re.findall(r'#([^#\s]*)', ranked)  # Extract double-quoted string values using regular expressions
            # rstr = ' '.join(map(str,ranked_str))
            rank = soup.find('span', attrs={'class': 'numbers ranked'}).text
            rank_str = [text for text in re.findall(r'[^]*(?<!Ranked)[]*', rank) if text]  # Extract double-quoted string values using regular expressions
            rst = ' '.join(map(str,rank_str))

            popularity = soup.find('span', attrs={'class': 'numbers popularity'}).text
            popular_str = [text for text in re.findall(r'[^]*(?<!Popularity)[]*', popularity) if text]  # Extract double-quoted string values using regular expressions
            pstr = ' '.join(map(str,popular_str))

            members = soup.find('span', attrs={'class': 'numbers members'}).text
            member_str = [text for text in re.findall(r'[^]*(?<!Members)[]*', members) if text]  # Extract double-quoted string values using regular expressions
            mstr = ' '.join(map(str,member_str))

            favorites = soup.find('div', attrs={'class': 'spaceit_pad'}).text
            # fav = favorites.find('')

            synopsis = soup.find('div', attrs={'class': 'spaceit_pad'}).text


        
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
            # st.image(image)
            # st.markdown("Scores:   {}".format(b,b))
            st.metric("Scores: ", score)

            st.metric("Ranked", rst)
            
            st.metric("Popularity", pstr)

            st.write("Members: ", mstr)
            ''' '''
            # st.write("Favourite: ", favorites)

            st.text(synopsis)
    

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