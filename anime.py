import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from scipy.spatial.distance import cdist
import requests
from bs4 import BeautifulSoup
import re
from anime_extractor import extract_anime_titles, extract_anime_url, extract_anime_images
# from kmean import topf

# anime_clean.csv
# csv_file_path = 'anime_clean.csv'
# # Extract anime titles using the separate module
# anime_titles = extract_anime_titles(csv_file_path)
# anime_urls = extract_anime_url(csv_file_path)

data = pd.read_csv("anime_clean.csv", encoding="utf8")
# print(data.head())

data = data.dropna(subset=['genres'])
data = data.dropna(subset=['source_type'])
data = data.dropna(subset=['studios'])
data = data.dropna(subset=['score'])

scaler = MinMaxScaler()

le = LabelEncoder()

df = data[['score','genres','studios']].copy()

df_with_id = data[['anime_id','title','score','genres','studios']].copy()

df['score'] = scaler.fit_transform(df[['score']])
df['genres'] = df['genres'].str.replace('|',', ')
df['genres'] = df['genres'].str.split(', ')
df = df.explode('genres')

df_with_id['score'] = scaler.fit_transform(df_with_id[['score']])
df_with_id['genres'] = df_with_id['genres'].str.replace('|',', ')
df_with_id['genres'] = df_with_id['genres'].str.split(', ')
df_with_id = df_with_id.explode('genres')


df['genres'] = le.fit_transform(df['genres'])
df['studios'] = le.fit_transform(df['studios'])

df_with_id['genres'] = le.fit_transform(df_with_id['genres'])
df_with_id['studios'] = le.fit_transform(df_with_id['studios'])

# print(df)

model = KMeans(n_clusters=3)
model.fit(df)


# Extract anime titles using the separate module
csv_file_path = 'anime_clean.csv'
# Extract anime titles using the separate module
anime_titles = extract_anime_titles(csv_file_path)
anime_urls = extract_anime_url(csv_file_path)
anime_imgs = extract_anime_images(csv_file_path)


def display_dt():

    url = ''
    b = 6.39

    # Dataframe Anime list 
    dff = pd.DataFrame({
        "Anime": ["a", "b", "c", "d", "e", "f"],
        "Similarity Scores (based on users)": [0.1264, 0.1244, 0.2344, 0.1944, 0.4422, 0.3012],
    })


    ################## Main UI layout ##################

    st.title("Animatch")
    with st.expander("Tap to select an Animes 🌀", expanded=True):
        choice = st.selectbox("", anime_titles)
        
        # Get the corresponding URL for the selected anime
        selected_url = anime_urls[anime_titles.index(choice)]

        # Scrap from corresponded url
        if selected_url in anime_urls:
            # Find where new point is locate in which cluster and find distance between points from chosen point
            anime_name = choice
            if anime_name in df_with_id['title'].values:
                row = df_with_id[df_with_id['title'] == anime_name].copy().drop_duplicates(subset='anime_id')
                
                # print(row)

                encoded = row[['score','genres','studios']].values
                # print(encoded)

                # new_point = np.array([[row[['score','genres','studios']].values]])
                nearest_cluster  = model.predict(encoded)

                # current data is from 696
                cluster_recommended_data = df[model.labels_ == nearest_cluster]

                top5 = []

                for index, row in cluster_recommended_data.iterrows():
                    cluster_point = np.array([[row['score'], row['genres'], row['studios']]])
                    distance = cdist(encoded, cluster_point)
                    
                    # Add the index and distance to top5 list
                    top5.append((index, distance[0][0]))

                # Sort the top5 list based on distance
                top5.sort(key=lambda x: x[1])

                # Keep only the top 5 unique distances and remove duplicates
                unique_distances = set()
                filtered_top5 = []
                for idx, dist in top5:
                    if dist not in unique_distances:
                        filtered_top5.append((idx, dist))
                        unique_distances.add(dist)
                    if len(filtered_top5) >= 5:
                        break

                # print(filtered_top5)
                    
                top5_ids = []
                for item in filtered_top5:
                    top5_ids.append(item[0])

                final_df = df_with_id.loc[top5_ids].copy()
                final_df = final_df.drop_duplicates(subset='anime_id')


            # Append image
            
            url += selected_url
        
            # request allow you to send HTTP request
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')  # main scraping

            # Elements to display under anime statistics
            score = soup.find('span', class_="score-label").text     
            
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

    st.text("")
    st.text("")
    if is_clic:
        if anime_name in df_with_id['title'].values:
            st.text("Here are a few similar animes recommendations  ◕⩊◕")

            # st.write(final_df)
            st.dataframe(final_df,use_container_width=True)
        else:
            st.text("")
            st.text("")

        st.text("")
        st.text("")
        st.text("")

        st.header(choice)
        st.write(url)
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