from django.db import models

# Create your models here.

class Movie(models.Model):
    class Genre(models.TextChoices):
        ACTION = 'action', 'Action'
        COMEDY = 'comedy', 'Comedy'
        DRAMA = 'drama', 'Drama'
        SCIFI = 'scifi', 'Sici-Fi'
        HORROR = 'horror', 'Horror'
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster_url = models.URLField()
    tmdb_id = models.IntegerField(unique=True)
    genre = models.CharField(max_length=20, choices=Genre.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']