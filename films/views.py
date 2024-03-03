from django.http.response import HttpResponse
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model

from films.forms import RegisterForm
from films.models import Film


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class Login(LoginView):
    template_name = 'registration/login.html'


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


class FilmListView(ListView):
    template_name = 'films.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Film.objects.none()
        user = self.request.user
        return user.films.all()


def check_username(request):
    """Return Response"""
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div id="username-error" class="error">Username already exists</div>', status=200)
    return HttpResponse('<div id="username-error" class="success">Username is available</div>', status=200)


def add_film(request):
    name = request.POST.get('filmname')

    film, is_new = Film.objects.get_or_create(name=name)
    # add the film to the user's list
    request.user.films.add(film)

    # return template with all user's films
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})
