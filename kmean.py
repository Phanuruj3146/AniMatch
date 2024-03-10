import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from scipy.spatial.distance import cdist


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

print(df)

model = KMeans(n_clusters=3)
model.fit(df)

# print(df_with_id.head())

# silhouette_score(df, model.labels_)

# Find where new point is locate in which cluster and find distance between points from chosen point
anime_name = str(input("What's the aniname >"))
if anime_name in df_with_id['title'].values:
    row = df_with_id[df_with_id['title'] == anime_name].copy().drop_duplicates(subset='anime_id')

# print(row)

encoded = row[['score','genres','studios']].values
print(encoded)


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

print(final_df)
# return final_df

