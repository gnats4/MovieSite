from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField()
    release_date = models.DateField(null=True, blank=True)

    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name="movies")
    director = models.ForeignKey(Director, on_delete=models.PROTECT, related_name="movies")

    imdb_url = models.URLField(blank=True)
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)

    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    synopsis = models.TextField(blank=True)

    review_text = models.TextField(blank=True)
    user_rating = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
