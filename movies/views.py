from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Movie, Genre, Director
from django.core.paginator import Paginator



def home(request):
    return render(request, "movies/home.html")

def about(request):
    return render(request, "movies/about.html")

def movie_list(request):
    q = request.GET.get("q", "").strip()
    genre_id = request.GET.get("genre", "")
    director_id = request.GET.get("director", "")
    sort = request.GET.get("sort", "title")

    movies = Movie.objects.all().select_related("genre", "director")

    if q:
        movies = movies.filter(Q(title__icontains=q) | Q(synopsis__icontains=q))

    if genre_id:
        movies = movies.filter(genre_id=genre_id)

    if director_id:
        movies = movies.filter(director_id=director_id)

    if sort == "imdb":
        movies = movies.order_by("-imdb_rating", "title")
    else:
        movies = movies.order_by("title")

    paginator = Paginator(movies, 1)  # 8 ταινίες ανά σελίδα
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "movies": page_obj,  # για να δουλεύει όπως πριν το template σου
        "genres": Genre.objects.all().order_by("name"),
        "directors": Director.objects.all().order_by("last_name", "first_name"),
        "q": q,
        "genre_id": genre_id,
        "director_id": director_id,
        "sort": sort,
    }
    return render(request, "movies/movie_list.html", context)

def movie_detail(request, pk):
    movie = get_object_or_404(Movie.objects.select_related("genre", "director"), pk=pk)
    return render(request, "movies/movie_detail.html", {"movie": movie})
