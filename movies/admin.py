from django.contrib import admin
from .models import Movie, Favorite, Review
# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'poster_url', 'tmdb_id', 'genre', 'created', 'updated')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'text', 'rating', 'created')
    list_filter = ('movie', 'user')
    search_fields = ('movie__title', 'user__username')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created')