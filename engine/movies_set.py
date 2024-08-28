import os
import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# JSON 파일 읽기
file_path = 'D:\StartPython\OTT_recommend_AI\engine\data\db_4.json'


with open(file_path, 'r',encoding='UTF8') as file:
    data = json.load(file)

df = pd.json_normalize(data)
df5=df.copy()
def create_soup(x):
    genres = ' '.join(str(item) for item in x['fields.genres'])
    actors = ' '.join(str(item) for item in x['fields.actors'])
    directors = ' '.join(str(item) for item in x['fields.directors'])
    keywords = ' '.join(str(item) for item in x['fields.keywords'])
    overview = ' '.join(str(item) for item in x['fields.overview'])


    return f"{genres}  {actors}  {directors}  {keywords} {overview}"
df5['soup'] = df5.apply(create_soup, axis=1)

#코사인유사도
indices=pd.Series(df5.index,index=df5['fields.title']).drop_duplicates()
count=CountVectorizer(stop_words='english')
count_matrix=count.fit_transform(df5['soup'])
cosine_sim2=cosine_similarity(count_matrix,count_matrix)

#영화추천 함수
def get_recommendations(title):

  idx=indices[title]#영화제목을 통해 그 영화의 인덱스 값을 얻어옴

  sim_scores=list(enumerate(cosine_sim2[idx]))#해당 인덱스에 대해서 다른 인덱스들의 유사도를 구하는 방법

  sim_scores=sorted(sim_scores,key=lambda x: x[1],reverse=True)# 코사인 유사도 기준으로 내림차순으로 정열하는 방법
  #sorted(test_sim_scores)된 값의 2번째 값(유사도)를 가져와서 내림차순으로 정렬하겠다는 의미

  sim_scores=sim_scores[0:10]#자기 자신을 제외한 비슷한 영화 10개를 추천한다

  movie_indices=[i[0] for i in sim_scores]#sim_scores여기에 해당하는 영화들의 인덱스를 추출

  pddf = df5[['fields.title', 'fields.poster_path']].iloc[movie_indices]#인덱스 정보를 통해 영화 제목을 가져옴

  title = pd.DataFrame(pddf)
  movie_title = title['fields.title'].tolist()
  movie_post = title['fields.poster_path'].tolist()
  movie_list = dict(zip(movie_title, movie_post))
  return movie_list

def get_movies_by_genre(genre_code):
    # Path to the JSON file
    json_file_path = "D:\\StartPython\\OTT_recommend_AI\\engine\\data\\db_4.json"

    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter movies by genre code
    movies = [movie for movie in data if genre_code in movie['fields']['genres']]

    return movies