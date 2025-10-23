from django.urls import path
from .views import CustomLoginView, CustomLogoutView, SignUpView, MovieListView, MovieDetailView, ReviewCreateView, ReviewListView, ReviewUpdateView, ReviewDeleteView, ProfileView, FavoriteView, FavoriteListView, FavoriteDeleteView

app_name='movies'

urlpatterns = [
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:pk>/reviews/', ReviewListView.as_view(), name='reviews'),
    path('movies/<int:pk>/reviews/<int:review_pk>/', ReviewUpdateView.as_view(), name='review_update'),
    path('movies/<int:pk>/reviews/', ReviewCreateView.as_view(), name='review_create'),
    path('movies/<int:pk>/reviews/<int:review_pk>/', ReviewDeleteView.as_view(), name='review_delete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/', FavoriteListView.as_view, name='favorites'),
    path('profile/<int:favorite_pk>/', FavoriteDeleteView.as_view(), name='favorite_delete'),
    path('favorite/', FavoriteView.as_view(), name='add_favorite'),
]
