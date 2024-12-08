# import the necessary libraries
import pandas as pd
from sklearn.cluster import KMeans


df = pd.read_csv('nbaallelo_log.csv')# load nbaallelo_log.csv into a dataframe

x = df[['pts', 'elo_i']]# subset the pts and elo_i columns

kmeans = KMeans(n_clusters=2, random_state=2)# create the clustering model with 2 clusters, use the parameter random_state = 2 to make reproducible
kmeans.fit(x)
print(kmeans.cluster_centers_)