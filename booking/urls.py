from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('movie_detail/', views.movie_detail, name="movie_detail"),
    path('login/', views.loginPage, name="loginPage"),
    path('register/', views.register, name="register"),
    path('logout/', views.logoutPage, name="logoutPage"),
]
