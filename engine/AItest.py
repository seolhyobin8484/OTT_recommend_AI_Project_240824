import os
import pandas as pd
import numpy as np

# u.tab 파일 읽기
base_src = 'C:\ml-100k\ml-100k' #경로 지정
u_user_src = os.path.join(base_src, 'u.tab')
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv(u_user_src,
                    sep='|', #구분자 기호
                    names=u_cols,
                    encoding='latin-1')
users = users.set_index('user_id')

# u.item 파일 읽기
u_item_src = os.path.join(base_src, 'u.item')
i_cols = ['movie_id', 'title', 'release data', 'video release data',
          'IMDB URL', 'unknown', 'Action', 'Adventure', 'Animation',
          'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
          'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
          'Thriller', 'War', 'Western']
movies = pd.read_csv(u_item_src,
                    sep='|', #구분자 기호
                    names=i_cols,
                    encoding='latin-1')
movies = movies.set_index('movie_id')

# u.data 파일 읽기
u_data_src = os.path.join(base_src, 'u.data')
r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv(u_data_src,
                    sep='\t', #구분자 기호
                    names=r_cols,
                    encoding='latin-1')
ratings = ratings.set_index('user_id')




# 인기제품 방식 추천 함수
def recom_movie(n_items):
    # 각 영화별로 평균 평점 계산
    movie_mean = ratings.groupby('movie_id')['rating'].mean()

    # 평점이 높은 순서로 정렬하고 상위 n_items 개 추출
    movie_sort = movie_mean.sort_values(ascending=False).head(n_items)

    # 영화 제목 추출을 위한 영화 데이터프레임에서 추천 영화 추출
    recom_movies = movies.loc[movie_sort.index]

    # 추천 영화 제목 반환
    recommendations = recom_movies['title']

    return recommendations
recom_movie(5) ### 평균 평점이 가장 높은 5개의 영화를 추천

def RMSE(y_true, y_pred):
    return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2))
# 정확도 계산
rmse = []
movie_mean = ratings.groupby(['movie_id'])['rating'].mean()

for user in set(ratings.index):
    # 해당 사용자가 평가한 영화 ID 목록
    movie_ids = ratings.loc[user]['movie_id']

    # 해당 사용자가 평가한 영화에 대한 실제 평점
    y_true = ratings.loc[user]['rating']

    # 각 영화에 대해 예측 평점 계산
    # movie_ids는 여러 개의 영화 ID를 포함할 수 있으므로, 각 영화 ID에 대해 평균 평점을 가져옴
    y_pred = movie_mean[movie_ids].values

    # 실제 평점과 예측 평점이 길이가 일치하는지 확인
    if len(y_true) == len(y_pred):
        # 정확도 계산
        accuracy = RMSE(y_true, y_pred)
        rmse.append(accuracy)

# RMSE 결과 출력
print(np.mean(rmse))

ratings = ratings.drop('timestamp', axis=1)
print(movies.columns)
movies = movies[['title']]

# 데이터 분할
from sklearn.model_selection import train_test_split

x = ratings.copy()
y = ratings['user_id']

x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size=0.25,
                                                    stratify=y)


# 모델별 RMSE를 계산하는 함수
def score(model):
    id_pairs = zip(x_test['user_id'], x_test['movie_id'])
    y_pred = np.array([model(user, movie) for (user, movie) in id_pairs])
    y_true = np.array(x_test['rating'])
    return RMSE(y_true, y_pred)


# train 데이터와 유저 정보 데이터 합치기
merged_ratings = pd.merge(x_train, users)

users = users.set_index('user_id')

# 성별 기준으로 평균 groupby
g_mean = merged_ratings[['movie_id', 'sex', 'rating']].groupby(['movie_id', 'sex'])['rating'].mean()

# ratings matrix 생성 : gender기준으로 추천할 때, 사용
rating_matrix = x_train.pivot(index='user_id',
                              columns='movie_id',
                              values='rating')