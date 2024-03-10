from django.urls import path

from gdp import views

urlpatterns = [
    path("", views.gdp_index, name="gdp_index"),
]
