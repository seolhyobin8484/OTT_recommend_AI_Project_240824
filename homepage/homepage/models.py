# from django.db import models
# from django.contrib.auth.models import User
#
# # models.py
#
# from django.db import models
#
# class Movie(models.Model):
#     title = models.CharField(max_length=200)
#     original_title = models.CharField(max_length=200)
#     overview = models.TextField()
#     vote_average = models.FloatField()
#     poster_path = models.CharField(max_length=255)  # poster_path를 문자열로 저장
#     runtime = models.IntegerField()
#     status = models.CharField(max_length=50)
#     tagline = models.CharField(max_length=255, blank=True, null=True)
#     genres = models.CharField(max_length=255)
#     keywords = models.CharField(max_length=255)
#     directors = models.CharField(max_length=255)
#     actors = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.title
#
# class Rating(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     rating = models.IntegerField()  # 1 to 5 scale
#
#     def __str__(self):
#         return f'{self.user.username} - {self.movie.title}: {self.rating}'
#
# class Review(models.Model):
#     author = models.CharField(max_length=100)
#     date = models.DateField()
#     views = models.IntegerField()
#     rating = models.FloatField()
#
#     def __str__(self):
#         return self.author
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

# models.py

from django.db import models

class Movie(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200)
    overview = models.TextField()
    vote_average = models.FloatField()
    poster_path = models.CharField(max_length=255)  # poster_path를 문자열로 저장
    runtime = models.IntegerField()
    status = models.CharField(max_length=50)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    genres = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    directors = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.TextField()
    post = models.TextField()
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField()
