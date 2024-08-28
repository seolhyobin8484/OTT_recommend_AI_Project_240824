import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from engine import databases, svd_code
from engine import movies_set as ms
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from django.http import Http404
from django.conf import settings

from .models import Movie
from .models import Comment
from django.utils import timezone
import pandas as pd


login_res = False
user_name = None
def save_session(request, id, password):
    request.session['id'] = id
    request.session['password'] = password

def get_post_login(request):
    if request.method == 'POST':
        id = request.POST['id']
        password = request.POST['password']

        global login_res, user_name
        login_res,user_name = databases.login_user(id,password)
        save_session(request, id, password)

        movies = svd_result()

        if login_res == True :
            return render(request, 'homepage.html',{'login_res': login_res, 'name': user_name, 'movies': movies} )
        return render(request, 'menu/login.html',{'login_res': login_res, 'name': user_name} )

def get_post_signup(request):
    if request.method == 'POST':
        id = request.POST['id']
        password = request.POST['password']
        name = request.POST['name']
        sex = request.POST['sex']
        genres = request.POST['genres']
        print(id, password, name, sex, genres)

        res = databases.insert_user(id,password,name,sex,genres)

        if res == True :
            return render(request, 'menu/login.html',{'res': res} )
        return render(request, 'menu/signup.html',{'res': res} )

def delete_table_if_count_mismatch(json_file_path):
    # JSON 파일 읽기
    with open(json_file_path, 'r', encoding='UTF8') as file:
        data = json.load(file)

    # JSON 데이터의 항목 수
    json_count = len(data)

    # Movie 테이블의 레코드 수
    movie_count = Movie.objects.count()

    # 수가 맞지 않으면 테이블 내용 삭제
    if json_count != movie_count:
        print(f"갯수가 맞지 않습니다! JSON: {json_count}, 테이블: {movie_count}. 테이블 내용을 삭제합니다.")
        Movie.objects.all().delete()
        load_json_to_movie_table(json_file_path)
    else:
        print("JSON 데이터와 Movie 테이블의 갯수가 일치합니다.")

def load_json_to_movie_table(json_file_path):
    # JSON 파일 읽기
    with open(json_file_path, 'r',encoding='UTF8') as file:
        data = json.load(file)

    for item in data:
        # 'fields'에서 데이터를 가져와 Movie 인스턴스를 생성합니다.
        fields = item['fields']

        Movie.objects.create(
            id=item['pk'],
            title=fields['title'],
            original_title=fields['original_title'],
            overview=fields['overview'],
            vote_average=fields['vote_average'],
            poster_path=fields['poster_path'],
            runtime=fields['runtime'],
            status=fields['status'],
            tagline=fields.get('tagline', ''),  # tagline은 빈 문자열로 기본값 설정
            genres=fields['genres'],  # 리스트로 저장된 장르 ID
            actors=fields['actors'],  # 리스트로 저장된 배우 ID
            directors=fields['directors'],  # 리스트로 저장된 감독 ID
            keywords=fields['keywords']  # 리스트로 저장된 키워드 ID
        )

    print("JSON 데이터를 Movie 테이블에 성공적으로 삽입했습니다.")

    movies = Movie.objects.all()
    for movie in movies:
        print(f"Title: {movie.title}")

def svd_result():
    file_path = "D:\\StartPython\\OTT_recommend_AI\\engine\\data\\db_4.json"
    delete_table_if_count_mismatch(file_path)
    reco_list = svd_code.get_recommend(1)
    m_list = []
    for i in reco_list:
        movie = svd_code.get_movies_by_pk(i)
        m_list.append(movie)
    return m_list

def homepage(request):
    movies = svd_result()
    return render(request, 'homepage.html', {'login_res': login_res, 'movies': movies, 'name' : user_name})
def login(request):
    return render(request, 'menu/login.html',{'login_res': None})


def signup(request):
    return render(request, 'menu/signup.html',{'login_res': login_res})

# def update_user_info(request):
#     if request.method == 'POST':
#         id = request.POST['id']
#         password = request.POST['password']
#         name = request.POST['name']
#         sex = request.POST['sex']
#         location = request.POST['location']
#
#         res = databases.update_user_info(id, password, name, sex, location)


def notice(request):
    global login_res
    if login_res == True :
        return render(request, 'menu/notice.html', {'login_res': True})
    return render(request, 'menu/notice.html', {'login_res': False})

def aboutus(request):
    return render(request, 'menu/aboutus.html',{'login_res': login_res})

def myinfo(request):
    global user_name

    comments = Comment.objects.filter(user=user_name)
    # title=Movie.objects

    return render(request, 'menu/myinfo.html',{'login_res': login_res, 'comments' : comments})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('myinfo')  # Redirect to the page listing comments
    return redirect('myinfo')  # Redirect to the page listing comments if method is not POST


def search(request):
    try:
        error = False
        input_data = request.GET.get('q')
        RE_movies = ms.get_recommendations(input_data)
        # print(input_data)
        # print(RE_movies)

    except:
        error = True
        return render(request, 'homepage.html', {'error': error})
    return render(request, 'recommendation.html',{'movies': RE_movies,'error': error} )



def recommend(request):
    try:
        error = False
        input_data = request.GET.get('q')
        RE_movies = ms.get_recommendations(input_data)
        # print(input_data)
        # print(RE_movies)

    except:
        error = True
        return render(request, 'homepage.html', {'error': error})
    return render(request, 'recommendation.html', {'movies': RE_movies, 'error': error})

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def detailpage(request, movie_id):
    # Load data from JSON files
    movies_data = load_json(os.path.join("D:\\StartPython\\OTT_recommend_AI\\engine\\data\\db_4.json"))
    all_data = load_json(os.path.join("D:\\StartPython\\OTT_recommend_AI\\engine\\data\\db_5.json"))

    # Find the movie with the given string ID
    movie = next((item for item in movies_data if item['fields']['title'] == movie_id and item['model'] == 'movies.movie'), None)

    if not movie:
        raise Http404("Movie not found")

    # Extract IDs
    actor_ids = set(movie['fields']['actors'])
    director_ids = set(movie['fields']['directors'])
    genre_ids = set(movie['fields']['genres'])
    keyword_ids = set(movie['fields']['keywords'])

    # Get actors and directors
    actors_data = [item for item in all_data if item['model'] == 'movies.actor' and item['pk'] in actor_ids]
    directors_data = [item for item in all_data if item['model'] == 'movies.director' and item['pk'] in director_ids]
    unique_actors = {actor['fields']['name']: actor for actor in actors_data}.values()
    unique_directors = {director['fields']['name']: director for director in directors_data}.values()

    # Get genres and keywords
    genres_data = [item for item in all_data if item['model'] == 'movies.genre' and item['pk'] in genre_ids]
    keywords_data = [item for item in all_data if item['model'] == 'movies.keyword' and item['pk'] in keyword_ids]

    genre_mapping = {item['pk']: item['fields']['name'] for item in genres_data}
    keyword_mapping = {item['pk']: item['fields']['name'] for item in keywords_data}

    movie_genres = [genre_mapping.get(genre_id, 'Unknown') for genre_id in movie['fields']['genres']]
    movie_keywords = [keyword_mapping.get(keyword_id, 'Unknown') for keyword_id in movie['fields']['keywords']]

    # Find other movies with the same genres
    same_genre_movies = [item for item in movies_data if
                         set(item['fields']['genres']).intersection(genre_ids) and item['fields']['title'] != movie_id]

    # Limit to 5 movies
    same_genre_movies = same_genre_movies[:5]

    total_minutes = movie['fields']['runtime']
    hours, minutes = divmod(total_minutes, 60)
    rating = movie['fields'].get('vote_average', 0)
    formatted_rating = f"{rating:.1f}"

    # Handle POST request for comments
    if request.method == "POST":
        Comment.objects.create(user=user_name, post=movie_id, body=request.POST['body'], date=timezone.now(),
                               rating=request.POST['rating'])

    post_detail = get_object_or_404(Movie, title=movie_id)
    comments = Comment.objects.filter(post=movie_id)

    context = {
        'hours': hours,
        'minutes': minutes,
        'movie': movie['fields'],
        'actors': unique_actors,
        'directors': unique_directors,
        'formatted_rating': formatted_rating,
        'genres': movie_genres,
        'keywords': movie_keywords,
        'same_genre_movies': same_genre_movies,
        'login_res': login_res,  # login_res should be defined elsewhere
        'tab': request.GET.get('tab', 'home'),  # default tab
        'post': post_detail,
        'comments': comments,
        # 'name': user_name
    }

    return render(request, 'detailpage.html', context)

def review_form(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # 리뷰 처리 로직 추가
            # 예: form.cleaned_data를 사용하여 데이터 저장
            rating = form.cleaned_data['rating']
            content = form.cleaned_data['content']
            # 데이터베이스에 저장하는 코드 작성
            # 예: Review.objects.create(rating=rating, content=content)
            return redirect('success')  # 리뷰 제출 후 리디렉션할 URL
    else:
        form = ReviewForm()

    return render(request, 'detailpage.html', {'form': form})


def action(request):
    genre_code = 28  # Genre code for animation
    movies = ms.get_movies_by_genre(genre_code)
    return render(request, 'genre/action.html', {'login_res': request.user.is_authenticated, 'movies': movies})
def comedy(request):
    genre_code = 35  # Genre code for animation
    movies = ms.get_movies_by_genre(genre_code)
    return render(request, 'genre/comedy.html', {'login_res': request.user.is_authenticated, 'movies': movies})
def horror(request):
    genre_code = 27  # Genre code for animation
    movies = ms.get_movies_by_genre(genre_code)
    return render(request, 'genre/horror.html', {'login_res': request.user.is_authenticated, 'movies': movies})
def romance(request):
    genre_code = 10749  # Genre code for animation
    movies = ms.get_movies_by_genre(genre_code)
    return render(request, 'genre/romance.html', {'login_res': request.user.is_authenticated, 'movies': movies})
def drama(request):
    genre_code = 18  # Genre code for animation
    movies = ms.get_movies_by_genre(genre_code)
    return render(request, 'genre/drama.html', {'login_res': request.user.is_authenticated, 'movies': movies})
def anime(request):
    genre_code = 16  # Genre code for animation
    movies = ms.get_movies_by_genre(genre_code)
    # 디버깅: 영화 ID와 제목 출력
    return render(request, 'genre/anime.html', {'login_res': request.user.is_authenticated, 'movies': movies})


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

import json
import os
from django.shortcuts import render
from django.http import Http404
from django.conf import settings

def get_coment(request):
    name = request.POST['coment']
    rating = request.POST['rating']

    return name


def detail_page(request, movie_id):
    movies_data = load_json(os.path.join("D:\\StartPython\\OTT_recommend_AI\\engine\\data\\db_4.json"))
    all_data = load_json(os.path.join("D:\\StartPython\\OTT_recommend_AI\\engine\\data\\db_5.json"))

    movie = next((item for item in movies_data if item['pk'] == movie_id and item['model'] == 'movies.movie'), None)

    if not movie:
        raise Http404("Movie not found")

    actor_ids = set(movie['fields']['actors'])
    director_ids = set(movie['fields']['directors'])
    genre_ids = set(movie['fields']['genres'])
    keyword_ids = set(movie['fields']['keywords'])

    # Get actors and directors
    actors_data = [item for item in all_data if item['model'] == 'movies.actor' and item['pk'] in actor_ids]
    directors_data = [item for item in all_data if item['model'] == 'movies.director' and item['pk'] in director_ids]
    unique_actors = {actor['pk']: actor for actor in actors_data}.values()
    unique_directors = {director['pk']: director for director in directors_data}.values()

    # Get genres and keywords
    genres_data = [item for item in all_data if item['model'] == 'movies.genre' and item['pk'] in genre_ids]
    keywords_data = [item for item in all_data if item['model'] == 'movies.keyword' and item['pk'] in keyword_ids]

    genre_mapping = {item['pk']: item['fields']['name'] for item in genres_data}
    keyword_mapping = {item['pk']: item['fields']['name'] for item in keywords_data}

    movie_genres = [genre_mapping.get(genre_id) for genre_id in movie['fields']['genres']]
    movie_keywords = [keyword_mapping.get(keyword_id, 'Unknown') for keyword_id in movie['fields']['keywords']]

    # Find other movies with the same genres
    same_genre_movies = [item for item in movies_data if
                         set(item['fields']['genres']).intersection(genre_ids) and item['pk'] != movie_id]

    # Limit to 5 movies
    same_genre_movies = same_genre_movies[:5]

    total_minutes = movie['fields']['runtime']
    hours, minutes = divmod(total_minutes, 60)
    rating = movie['fields'].get('vote_average', 0)
    formatted_rating = f"{rating:.1f}"

    if request.method == "POST":
        Comment.objects.create(user = user_name,post = movie_id, body = request.POST['body'],date = timezone.now(), rating = request.POST['rating'])

    post_detail = get_object_or_404(Movie,pk=movie_id)
    comments = Comment.objects.filter(post=movie_id)

    context = {
        'hours': hours,
        'minutes': minutes,
        'movie': movie['fields'],
        'actors': unique_actors,
        'directors': unique_directors,
        'formatted_rating': formatted_rating,
        'genres': movie_genres,
        'keywords': movie_keywords,
        'same_genre_movies': same_genre_movies,
        'login_res': login_res,  # login_res should be defined elsewhere
        'tab': request.GET.get('tab', 'home'), # default tab
        'post': post_detail,
        'comments': comments,
        'name': user_name
    }
    for genre_id in movie['fields']['genres'] :
        print(genres_data)
        print(genre_id)

        #숫자값 전달 o
        #숫자 - 문자 x

    return render(request, 'detailpage.html', context)

# def detail_page(request, movie_id):
#     movies_data = load_json(os.path.join("D:\\StartPython\\OTT_recommend_AI\\engine\\data\\db_4.json"))
#     all_data = load_json(os.path.join("D:\\StartPython\\OTT_recommend_AI\\engine\\data\\db_5.json"))
#
#
#     movie = next((item for item in movies_data if item['pk'] == movie_id and item['model'] == 'movies.movie'), None)
#
#     if not movie:
#         raise Http404("Movie not found")
#
#     actor_ids = set(movie['fields']['actors'])
#     director_ids = set(movie['fields']['directors'])
#     genre_ids = set(movie['fields']['genres'])
#     keyword_ids = set(movie['fields']['keywords'])
#
#     # Get actors and directors
#     actors_data = [item for item in all_data if item['model'] == 'movies.actor' and item['pk'] in actor_ids]
#     directors_data = [item for item in all_data if item['model'] == 'movies.director' and item['pk'] in director_ids]
#     unique_actors = {actor['pk']: actor for actor in actors_data}.values()
#     unique_directors = {director['pk']: director for director in directors_data}.values()
#
#     # Get genres and keywords
#     genres_data = [item for item in all_data if item['model'] == 'movies.genre' and item['pk'] in genre_ids]
#     keywords_data = [item for item in all_data if item['model'] == 'movies.keyword' and item['pk'] in keyword_ids]
#
#     genre_mapping = {item['pk']: item['fields']['name'] for item in genres_data}
#     keyword_mapping = {item['pk']: item['fields']['name'] for item in keywords_data}
#
#     movie_genres = [genre_mapping.get(genre_id, 'Unknown') for genre_id in movie['fields']['genres']]
#     movie_keywords = [keyword_mapping.get(keyword_id, 'Unknown') for keyword_id in movie['fields']['keywords']]
#
#     # Find other movies with the same genres
#     same_genre_movies = [item for item in movies_data if
#                          set(item['fields']['genres']).intersection(genre_ids) and item['pk'] != movie_id]
#
#     # Limit to 5 movies
#     same_genre_movies = same_genre_movies[:5]
#
#     total_minutes = movie['fields']['runtime']
#     hours, minutes = divmod(total_minutes, 60)
#     rating = movie['fields'].get('vote_average', 0)
#     formatted_rating = f"{rating:.1f}"
#
#     context = {
#         'hours': hours,
#         'minutes': minutes,
#         'movie': movie['fields'],
#         'actors': unique_actors,
#         'directors': unique_directors,
#         'formatted_rating': formatted_rating,
#         'genres': movie_genres,
#         'keywords': movie_keywords,
#         'same_genre_movies': same_genre_movies,
#         'login_res': login_res,  # login_res should be defined elsewhere
#         'tab': request.GET.get('tab', 'home')  # default tab
#     }
#     return render(request, 'detailpage.html', context)

def logout(request):
    auth_logout(request)  # Django의 내장 로그아웃 함수 호출
    return redirect('logout_done')  # 로그아웃 후 보여줄 페이지로 리디렉션

def logout_done(request):
    global login_res
    login_res = False
    return render(request, 'homepage.html',{'login_res' : login_res})  # 로그아웃 후 보여줄 페이지