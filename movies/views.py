from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm, ReviewForm
from .models import Movie, Review, Favorite
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.contrib.auth import login


class LogoutView(generic.View):
    def logout(request):
        return redirect('login')


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        return redirect('/')

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'register.html'
    initial = {'key': 'value'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')
    
class MovieListView(generic.ListView):
    model = Movie
    template_name = 'list.html'
    context_object_name = 'movie_list'
    paginate_by = 20

    def get_queryset(self):
        return Movie.objects.all()


class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'Movie'

    def get_queryset(self):
        return Movie.objects.filter(pk=self.kwargs['pk'])

class RevieCreateView(generic.CreateView):
    form_class = ReviewForm
    template_name = 'review_create.html'

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        review.movie.id = self.kwargs['pk']
        review.save()
        return redirect('movie_detail', pk=self.kwargs['pk'])

class ReviewListView(generic.ListView):
    model = Review
    template_name = 'movie_detail.html'

    def get_queryset(self):
        return Review.objects.filter(movie__id=self.kwargs['pk'])
    
class ReviewUpdate(generic.UpdateView):
    model = Review
    fields = ['text', 'rating']
    template_name = 'review_create.html'
    success_url = reverse_lazy('movie_detail')