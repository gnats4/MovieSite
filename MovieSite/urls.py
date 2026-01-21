from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def index(request):
    return redirect("movies:movie_list")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),  # 👈 homepage → movies
    path("movies/", include("movies.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
