import time

from django.db.models import Q
from django.shortcuts import render

from scores.models import Fixture


def fixtures(request):
    fixtures = Fixture.objects.select_related("home_team", "away_team").all()

    is_all_completed = all([fixture.game_finished for fixture in fixtures])

    search = request.GET.get("search")
    if search:
        fixtures = fixtures.filter(
            Q(home_team__name__icontains=search) | Q(away_team__name__icontains=search)
        )

    context = {"fixtures": fixtures, "is_all_completed": is_all_completed}
    if request.htmx:
        time.sleep(1.6)
        if is_all_completed:
            response = render(request, "partials/fixturelist.html", context, status=200)
            response["HX-Refresh"] = "true"
            return response
        return render(request, "partials/fixturelist.html", context)
    return render(request, "fixtures.html", context)
