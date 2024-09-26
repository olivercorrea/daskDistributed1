from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .appName("MovieLensAnalysis") \
    .master("spark://52.91.104.179:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://45.122.344:9000") \
    .getOrCreate()

start_time = time.time()

data = spark.read.csv('hdfs://52.91.104.179:9000/data/u.data', sep='\t', inferSchema=True, header=False) \
    .toDF('user_id', 'movie_id', 'rating', 'timestamp')
users = spark.read.csv('hdfs://52.91.104.179:9000/data/u.user', sep='|', inferSchema=True, header=False) \
    .toDF('user_id', 'age', 'gender', 'occupation', 'zip_code')
movies = spark.read.csv('hdfs://52.91.104.179:9000/data/u.item', sep='|', inferSchema=True, header=False) \
    .toDF('movie_id', 'movie_title', '_', '_', '_', '_', '_', '_', '_', '_')

data_merged = data.join(users, on='user_id').join(movies, on='movie_id')

movies_ranking = data_merged.groupBy('movie_title', 'age', 'occupation') \
    .agg({'rating': 'count', 'rating': 'mean'}) \
    .orderBy('count(rating)', ascending=False)

movies_ranking.show(10)

end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.2f} segundos")