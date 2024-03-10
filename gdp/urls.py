from django.urls import path

from gdp import views

urlpatterns = [
    path("bar/", views.gdp_index, name="gdp_index"),
    path("line/", views.gdp_line, name="gdp_line"),
]
