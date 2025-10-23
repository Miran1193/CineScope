from django.contrib import admin
from .models import Movie, Favorite, Review
# Register your models here.

@admin.site.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'poster_url', 'tmdb_id', 'genre', 'created', 'updated']

@admin.site.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'text', 'rating', 'created']


@admin.site.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'created']