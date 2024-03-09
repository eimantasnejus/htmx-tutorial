from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView

from films.forms import RegisterForm
from films.models import Film, UserFilms
from films.utils import get_max_order, reorder_user_films


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"


class Login(LoginView):
    template_name = "registration/login.html"


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


class FilmListView(LoginRequiredMixin, ListView):
    template_name = "films.html"
    model = UserFilms
    paginate_by = 2
    context_object_name = "user_films"

    def get_template_names(self):
        if self.request.htmx:
            return "partials/film-list-elements.html"
        return self.template_name

    def get_queryset(self):
        return UserFilms.objects.filter(user=self.request.user).order_by("order")


def check_username(request):
    """Return Response"""
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse('<div id="username-error" class="error">Username already exists</div>', status=200)
    return HttpResponse('<div id="username-error" class="success">Username is available</div>', status=200)


@login_required
def add_film(request):
    """Add film to user's list"""
    name = request.POST.get("filmname")

    # get or create the film
    film, is_new = Film.objects.get_or_create(name=name)

    # add the film to the user's list
    if not UserFilms.objects.filter(user=request.user, film=film).exists():
        UserFilms.objects.create(user=request.user, film=film, order=get_max_order(request.user))

    # return template with all user's films
    user_films = UserFilms.objects.filter(user=request.user).order_by("order")
    messages.success(request, f"{film.name} added to your list")
    return render(request, "partials/film-list.html", {"user_films": user_films})


@login_required
@require_http_methods(["DELETE"])
def delete_film(request, pk):
    """Remove film from user's list"""
    UserFilms.objects.filter(pk=pk).delete()

    # return template fragment
    reorder_user_films(request.user)
    user_films = UserFilms.objects.filter(user=request.user).order_by("order")
    return render(request, "partials/film-list.html", {"user_films": user_films})


def search_film(request):
    """Return search results"""
    search_text = request.POST.get("search")

    user_film_ids = UserFilms.objects.filter(user=request.user).values_list("film", flat=True)
    results = Film.objects.filter(name__icontains=search_text).exclude(pk__in=user_film_ids)
    context = {"results": results}
    return render(request, "partials/search-results.html", context)


def clear(request):
    return HttpResponse("<div></div>", status=200)


def reorder(request):
    """Update the order of user's films and return the updated list of films."""
    ordered_user_film_ids = request.POST.getlist("ordered_user_film_ids")
    user_films = []
    for i, user_film_pk in enumerate(ordered_user_film_ids, start=1):
        UserFilms.objects.filter(pk=user_film_pk).update(order=i)
        updated_user_film = UserFilms.objects.get(pk=user_film_pk)
        user_films.append(updated_user_film)
    return render(request, "partials/film-list.html", {"user_films": user_films})


@login_required
def film_detail(request, pk):
    user_film = get_object_or_404(UserFilms, user=request.user, pk=pk)
    context = {"user_film": user_film}
    return render(request, "partials/film-detail.html", context)


@login_required
def film_partial(request):
    user_films = UserFilms.objects.filter(user=request.user).order_by("order")
    return render(request, "partials/film-list.html", {"user_films": user_films})


@login_required
def upload_photo(request, pk):
    user_film = get_object_or_404(UserFilms, user=request.user, pk=pk)
    user_film.film.photo = request.FILES["photo"]
    user_film.film.save()
    return render(request, "partials/film-detail.html", {"user_film": user_film})
