from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from . import views

def root_redirect(request):
    return redirect('/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('homepage.html', root_redirect),
    path('login/', views.login, name='login'),
    path('homepage(tab)/', views.get_post_login, name='login_post'),
    path('signup/', views.signup, name='signup'),
    path('signup_post/', views.get_post_signup, name='signup_post'),
    path('notice/', views.notice, name='notice'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('logout/', views.logout, name='logout'),
    path('logout/done/', views.logout_done, name='logout_done'),
    path('action/', views.action, name='action'),
    path('comedy/', views.comedy, name='comedy'),
    path('horror/', views.horror, name='horror'),
    path('romance/', views.romance, name='romance'),
    path('drama/', views.drama, name='drama'),
    path('anime/', views.anime, name='anime'),
    path('detailpage/<int:movie_id>/', views.detail_page, name='detailpage_int'),
    path('detailpage/<str:movie_id>/', views.detailpage, name='detailpage_str'),
    path('search/', views.search, name='search'),
    path('recommend', views.recommend, name='recommend'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
