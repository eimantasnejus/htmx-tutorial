from django.shortcuts import render

from university.models import Course, Module


def courses(request):
    courses_qs = Course.objects.all()
    context = {"courses": courses_qs}
    return render(request, "university.html", context)


def modules(request):
    course = request.GET.get("course")
    modules = Module.objects.filter(course=course)
    return render(request, "partials/modules.html", {"modules": modules})