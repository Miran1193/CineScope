from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm, ReviewForm
from .models import Movie, Review, Favorite
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.contrib.auth import login
from django.db.models import Avg


class CustomLogoutView(LogoutView):

    def logout(request):
        return redirect(to='movies:login/')


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('movies:movies/')

    def form_valid(self, form):
        return super(CustomLoginView, self).form_valid(form)

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'register.html'
    initial = {'key': 'value'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('movies:movies/')
    
class MovieListView(generic.ListView):
    model = Movie
    template_name = 'list.html'
    context_object_name = 'movies'
    paginate_by = 20

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


class ReviewCreateView(generic.CreateView):
    form_class = ReviewForm
    template_name = 'review_create.html'

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        review.movie.id = self.kwargs['pk']
        review.save()
        return redirect('movie_detail', kwargs={'pk': self.kwargs['pk']})


class ReviewListView(generic.ListView):
    model = Review
    template_name = 'movie_detail.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(movie__pk=self.kwargs['pk'])
    
    def avg(self):
        return Review.objects.filter(movie__pk=self.kwargs['pk']).aaggregate(avg=Avg('rating'))


class ReviewUpdateView(generic.UpdateView):
    model = Review
    fields = ['text', 'rating']
    template_name = 'review_create.html'
    
    def get_success_url(self):
        return reverse_lazy('ovie_detail', kwargs={'pk': self.kwargs['pk']})


class ReviewDeleteView(generic.DeleteView):
    model = Review
    success_url = reverse_lazy('movie_detail')

    def get_queryset(self):
        return Review.objects.filter(pk=self.kwargs['pk'])
    
    def get_success_url(self):
        return reverse_lazy('movie_detail', kwargs={'pk': self.kwargs['pk']})
    

class FavoriteView(generic.CreateView):
    model = Favorite

    def post(self, request, *args, **kwargs):
        return Favorite.objects.create(movie=self.kwargs['movie_favorite.pk'], user=self.request.user)
    

class FavoriteListView(generic.ListView):
    model = Favorite
    template_name = 'profile.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    

class FavoriteDeleteView(generic.DeleteView):
    model = Favorite
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return Favorite.objects.filter(pk=self.kwargs['pk'])
    

class ProfileView(generic.View):
    model = User
    template_name = 'profile.html'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user)
    
    