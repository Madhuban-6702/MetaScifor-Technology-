from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone_number']  # Fields required during user creation

    def __str__(self):
        return self.email

class Anime(models.Model):
    anime_id = models.IntegerField(primary_key=True)  # Primary key
    name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255, blank=True, null=True)
    other_name = models.CharField(max_length=255, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)  # Genres can have multiple values
    synopsis = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    episodes = models.IntegerField(blank=True, null=True)
    aired = models.CharField(max_length=255, blank=True, null=True)
    premiered = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    producers = models.TextField(blank=True, null=True)  # Can have multiple values
    licensors = models.TextField(blank=True, null=True)
    studios = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    popularity = models.IntegerField(blank=True, null=True)
    favorites = models.IntegerField(blank=True, null=True)
    scored_by = models.IntegerField(blank=True, null=True)
    members = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # Store image URL

    def __str__(self):
        return self.name

class Watchlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    animes = models.ManyToManyField(Anime, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Watchlist"