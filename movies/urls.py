from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("movies/", views.movie_list, name="movie_list"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
]