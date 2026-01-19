from django.contrib import admin
from .models import Genre, Director, Movie

admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Movie)