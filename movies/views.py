from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Movie, Genre, Director


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

    paginator = Paginator(movies, 1)  # άλλαξέ το π.χ. σε 8 όταν βάλεις πολλές ταινίες
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "movies": page_obj,
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

    avg_rating = movie.reviews.aggregate(avg=Avg("rating"))["avg"]

    # Αν υπάρχει review του user, το φορτώνουμε για edit, αλλιώς νέο
    user_review = None
    if request.user.is_authenticated:
        user_review = movie.reviews.filter(user=request.user).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, "Το review σου αποθηκεύτηκε!")
            return redirect("movies:movie_detail", pk=movie.pk)
    else:
        form = ReviewForm(instance=user_review)

    context = {
        "movie": movie,
        "avg_rating": avg_rating,
        "form": form,
        "user_review": user_review,
    }
    return render(request, "movies/movie_detail.html", context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ο λογαριασμός δημιουργήθηκε! Κάνε login.")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})