import dask.dataframe as dd
from dask.distributed import Client
import time

client = Client('<scheduler-ip>:8786')

start_time = time.time()

data = dd.read_csv('/mnt/nfs_client/ml-100k/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
users = dd.read_csv('/mnt/nfs_client/ml-100k/u.user', sep='|', names=['user_id', 'age', 'gender', 'occupation', 'zip_code'])
movies = dd.read_csv('/mnt/nfs_client/ml-100k/u.item', sep='|', encoding='latin-1', header=None, usecols=[0, 1], names=['movie_id', 'movie_title'])

data_merged = dd.merge(data, users, on='user_id')
data_merged = dd.merge(data_merged, movies, on='movie_id')

movies_ranking = data_merged.groupby(['movie_title', 'age', 'occupation']).agg({
    'rating': ['count', 'mean']
}).compute().reset_index()

top_voted_movies = movies_ranking.sort_values(by=('rating', 'count'), ascending=False)

print(top_voted_movies.head(10))

end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.2f} segundos")