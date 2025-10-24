from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Movie(models.Model):
    class Genre(models.TextChoices):
        ACTION = 'action', 'Action'
        COMEDY = 'comedy', 'Comedy'
        DRAMA = 'drama', 'Drama'
        SCIFI = 'scifi', 'Sici-Fi'
        HORROR = 'horror', 'Horror'
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True)
    tmdb_id = models.IntegerField(unique=True)
    genre = models.CharField(max_length=20, choices=Genre.choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='review_movie')
    text = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Валидация происходит здесь, до сохранения
        if self.rating and (self.rating < 1 or self.rating > 10):
            raise ValidationError('Оценка должна быть от 1 до 10')

    def save(self, *args, **kwargs):
        # Вызов метода clean() для валидации перед сохранением
        self.clean()
        super().save(*args, **kwargs)
   
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    
    class Meta:
        ordering = ['-created']


    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favorite')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} like is {self.movie.title}"

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-created']