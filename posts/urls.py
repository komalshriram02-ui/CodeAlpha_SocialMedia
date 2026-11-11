from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("like/<int:post_id>/", views.toggle_like, name="toggle_like"),
]