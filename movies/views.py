from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm, ReviewForm
from .models import Movie, Review, Favorite
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.contrib.auth import login
from django.db.models import Avg
from .load_movies import save_movies_to_db
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction



class CustomLogoutView(LogoutView):

    def logout(request):
        return redirect(to='movies:login')


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('movies:movies')

    def form_valid(self, form):
        return super(CustomLoginView, self).form_valid(form)

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'register.html'
    initial = {'key': 'value'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('movies:movies')
    
class MovieListView(generic.ListView):
    model = Movie
    template_name = 'list.html'
    context_object_name = 'movies'
    paginate_by = 10

    def get_queryset(self):
        return Movie.objects.all()


class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'movie'

    def get_queryset(self):
        return Movie.objects.filter(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(movie=self.object)
        user = self.request.user
        context['is_favorite'] = False
        if user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(user=user, movie=self.object).exists()
        return context


class ReviewCreateView(generic.CreateView):
     form_class = ReviewForm
     template_name = 'review_create.html'

     def form_valid(self, form):
         review = form.save(commit=False)
         review.user = self.request.user
         review.movie_id = self.kwargs['pk']
         review.save()
         return redirect('movies:movie_detail', pk=self.kwargs['pk'])


class ReviewListView(generic.ListView):
    model = Review
    template_name = 'movie_detail.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(movie__id=self.kwargs['pk'])
    
    def avg(self):
        return Review.objects.filter(movie__id=self.kwargs['pk']).aaggregate(avg=Avg('rating'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = Movie.objects.get(pk=self.kwargs['pk'])
        return context

class ReviewUpdateView(generic.UpdateView):
    model = Review
    fields = ['text', 'rating']
    template_name = 'review_create.html'
    
    def get_object(self):
        # Получаем параметры из URL
        review_pk = self.kwargs.get('review_pk')
        movie_pk = self.kwargs.get('pk')

        # Используем get_object_or_404 для поиска объекта по двум параметрам
        # Это более безопасный и правильный способ
        return get_object_or_404(Review, pk=review_pk, movie=movie_pk)

    def get_success_url(self):
        return reverse_lazy('movies:movie_detail', kwargs={'pk': self.kwargs['pk']})

class ReviewDeleteView(generic.DeleteView):
    model = Review
    context_object_name = 'reviews'

    def get_object(self):
        review_pk = self.kwargs.get('review_pk')
        movie_pk = self.kwargs.get('pk')

        return get_object_or_404(Review, pk=review_pk, movie=movie_pk)
    
    def get_success_url(self):
        return reverse_lazy('movies:movie_detail', pk=self.kwargs['pk'])
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['movie'] = Movie.objects.get(pk=self.kwargs['pk'])
    #     return context
    


class ToggleFavoriteView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user

        with transaction.atomic():
            fav = Favorite.objects.filter(user=user, movie=movie).first()
            if fav:
                fav.delete()
            else:
                Favorite.objects.create(user=user, movie=movie)

        return redirect('movies:movie_detail', pk=movie.pk)

class FavoriteListView(generic.ListView):
    model = Favorite
    template_name = 'profile.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.request.user.pk)
        return context    


    
    