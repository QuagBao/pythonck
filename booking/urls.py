from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('movie_detail/', views.movie_detail, name="movie_detail")
]
