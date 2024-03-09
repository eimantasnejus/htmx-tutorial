from django.db.models import Max

from films.models import UserFilms


def get_max_order(user):
    """Return the highest order number for a user's films

    Default to 1 if no films are found.
    """
    return (UserFilms.objects.filter(user=user).aggregate(Max("order"))["order__max"] or 0) + 1


def reorder_user_films(user):
    """Reorder the user's films so that they are in sequential order starting from 1."""
    order = 1
    for user_film in UserFilms.objects.filter(user=user).order_by("order"):
        user_film.order = order
        user_film.save()
        order += 1
