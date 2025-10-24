from django.urls import path
from movies.views import CustomLoginView, CustomLogoutView, SignUpView, MovieListView, MovieDetailView, ReviewCreateView, ReviewListView, ReviewUpdateView, ReviewDeleteView, ToggleFavoriteView, FavoriteListView

app_name='movies'

urlpatterns = [
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:pk>/', ReviewListView.as_view(), name='reviews'),
    path('movies/<int:pk>/reviews/<int:review_pk>/update', ReviewUpdateView.as_view(), name='review_update'),
    path('movies/<int:pk>/reviews/create', ReviewCreateView.as_view(), name='review_create'),
    path('movies/<int:pk>/reviews/<int:review_pk>/delete', ReviewDeleteView.as_view(), name='review_delete'),
    path('profile/', FavoriteListView.as_view(), name='favorites'),
    path('movies/<int:pk>/favorite', ToggleFavoriteView.as_view(), name='toggle_favorite'),
]
