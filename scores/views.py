import time

from django.shortcuts import render

from scores.models import Fixture


def fixtures(request):
    fixtures = Fixture.objects.all()

    is_all_completed = all([fixture.game_finished for fixture in fixtures])
    context = {"fixtures": fixtures, "is_all_completed": is_all_completed}
    if request.htmx:
        time.sleep(1.6)
        if is_all_completed:
            response = render(request, "partials/fixturelist.html", context, status=200)
            response["HX-Refresh"] = "true"
            return response
        return render(request, "partials/fixturelist.html", context)
    return render(request, "fixtures.html", context)
