from django.urls import path

from scores import views

urlpatterns = [
    path("fixtures/", views.fixtures, name="fixtures"),
]
