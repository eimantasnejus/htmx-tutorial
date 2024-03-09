from django.core.management import BaseCommand

from university.models import Course, Module


class Command(BaseCommand):
    help = "Load Courses and Modules"

    def handle(self, *args, **kwargs):
        Module.objects.all().delete()
        course_names = [
            "Computer Science",
            "Mathematics",
            "Physics",
            "Film Study",
        ]

        if not Course.objects.exists():
            for course_name in course_names:
                Course.objects.create(name=course_name)

        cs = Course.objects.get(name="Computer Science")
        compsci_modules = [
            "AI",
            "Machine Learning",
            "Web Development",
            "Software Engineering",
            "NoSQL Databases",
        ]

        for module_name in compsci_modules:
            Module.objects.create(name=module_name, course=cs)

        maths = Course.objects.get(name="Mathematics")
        maths_modules = [
            "Algebra",
            "Calculus",
            "Statistics",
            "Differential Equations",
        ]

        for module_name in maths_modules:
            Module.objects.create(name=module_name, course=maths)

        physics = Course.objects.get(name="Physics")
        physics_modules = [
            "Quantum Mechanics",
            "Relativity",
            "Astrophysics",
            "Nuclear Physics",
        ]

        for module_name in physics_modules:
            Module.objects.create(name=module_name, course=physics)

        film = Course.objects.get(name="Film Study")
        film_modules = [
            "Directing",
            "Cinematography",
            "Editing",
            "Screenwriting",
        ]

        for module_name in film_modules:
            Module.objects.create(name=module_name, course=film)
