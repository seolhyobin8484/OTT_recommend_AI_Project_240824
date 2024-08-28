# # views.py
# from django.shortcuts import render, redirect
# from pymysql import cursors
# import os,sys
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
# from engine import databases
# from django.contrib.auth import logout as auth_logout
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from django.shortcuts import render
# from django.http import JsonResponse
# import json
# from django.conf import settings
# from django.http import Http404
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
# file_path = 'C:\OTT_recommend_AI\homepage\homepage\db_4.json'
#
#
# with open(file_path, 'r',encoding='UTF8') as file:
#     data = json.load(file)
#
# df = pd.json_normalize(data)
# df5=df.copy()
#
# def create_soup(x):
#     genres = ' '.join(str(item) for item in x['fields.genres'])
#     actors = ' '.join(str(item) for item in x['fields.actors'])
#     directors = ' '.join(str(item) for item in x['fields.directors'])
#     keywords = ' '.join(str(item) for item in x['fields.keywords'])
#     overview = ' '.join(str(item) for item in x['fields.overview'])
#
#     return f"{genres}  {actors}  {directors}  {keywords} {overview}"
# df5['soup'] = df5.apply(create_soup, axis=1)
#
# #코사인유사도
# indices=pd.Series(df5.index,index=df5['fields.title']).drop_duplicates()
# count=CountVectorizer(stop_words='english')
# count_matrix=count.fit_transform(df5['soup'])
# cosine_sim2=cosine_similarity(count_matrix,count_matrix)
# #영화추천 함수
# def get_recommendations(title):
#
#   idx=indices[title]#영화제목을 통해 그 영화의 인덱스 값을 얻어옴
#
#   sim_scores=list(enumerate(cosine_sim2[idx]))#해당 인덱스에 대해서 다른 인덱스들의 유사도를 구하는 방법
#
#   sim_scores=sorted(sim_scores,key=lambda x: x[1],reverse=True)# 코사인 유사도 기준으로 내림차순으로 정열하는 방법
#   #sorted(test_sim_scores)된 값의 2번째 값(유사도)를 가져와서 내림차순으로 정렬하겠다는 의미
#
#   sim_scores=sim_scores[1:11]#자기 자신을 제외한 비슷한 영화 10개를 추천한다
#
#   movie_indices=[i[0] for i in sim_scores]#sim_scores여기에 해당하는 영화들의 인덱스를 추출
#
#   pddf = df5[['fields.title', 'fields.poster_path']].iloc[movie_indices]#인덱스 정보를 통해 영화 제목을 가져옴
#
#   title = pd.DataFrame(pddf)
#   movie_title = title['fields.title'].tolist()
#   movie_post = title['fields.poster_path'].tolist()
#   movie_list = movie_title+movie_post
#   return movie_list[:11]
#
# # print(get_recommendations('스노우 독스'))
# a=get_recommendations('스노우 독스')
# print(a)
import pandas as pd
import pickle
from surprise import SVD, Dataset, Reader

# 파일 경로 설정
ratings_file_path = "D:\\StartPython\\OTT_recommend_AI\\engine\\data\\movies.pkl"
svd_file_path = "D:\\StartPython\\OTT_recommend_AI\\engine\\data\\svd.pkl"

# 데이터 로드
ratings = pd.read_pickle(ratings_file_path)

# 모델 로드
with open(svd_file_path, 'rb') as f:
    svd = pickle.load(f)

# 예측을 위한 데이터 준비
# Note: 예측하려는 특정 user_id와 item_id가 필요합니다.
# 예를 들어, user_id = 1, item_id = 862

# 데이터 준비
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# 모델을 사용할 준비
# 여기서는 모델이 이미 로드되어 있으므로 학습은 필요 없습니다.
# 하지만 실제 예측을 위해서는 이미 훈련된 모델이 필요합니다.

# 예측을 수행
# user_id = 1
# item_id = 862

# SVD 모델을 사용하여 예측
# prediction = svd.predict(user_id, item_id)
# print(prediction)


# print(ratings['movieId'])
# user_rating=ratings[ratings['userId']==2]
# print(type(user_rating['movieId']))
# a=user_rating['movieId'].tolist()
# print(a)


# views.py
from django.shortcuts import render, redirect
from pymysql import cursors
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from engine import databases
from django.contrib.auth import logout as auth_logout
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from django.conf import settings
from django.http import Http404
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homepage.homepage.settings")

import django
django.setup()
import random
def get_recommend(user_id):
  user_rating=ratings[ratings['userId']==user_id]
  ratings_mwiveId=ratings['movieId'].tolist()
  user_movieId=user_rating['movieId'].tolist()
  rating_list = []

  # 영화 ID를 순회합니다.
  for movie_id in ratings_mwiveId:
      # 예측 결과를 가져옵니다.
      if movie_id not in user_movieId:
        prediction = svd.predict(user_id, movie_id)
        # print(movie_id)
      # print(prediction)
      # 평점을 확인하고, 평점이 4 이상인 경우 영화 ID를 추가합니다.
        if prediction.est >= 4:
            rating_list.append(movie_id)
  # 예측 결과를 (item_id, predicted_rating) 튜플 리스트로 변환
  return rating_list[:10]

rating_list=get_recommend(2)

print(rating_list)


def get_movies_by_pk(genre_code):
    # Path to the JSON file
    json_file_path = "D:\\StartPython\\OTT_recommend_AI\\engine\\data\\db_4.json"

    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter movies by genre code
    movie = next((item for item in data if item['pk'] == genre_code and item['model'] == 'movies.movie'), None)
    return movie
movies=get_movies_by_pk(5503)

# print(movies.fileds.poster_path)

m_list=[]
for i in rating_list:
    movie=get_movies_by_pk(i)
    m_list.append(movie)

print(m_list[1])
