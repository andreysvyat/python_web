from django.urls import path

from . import views

urlpatterns = [
    path("headers", views.show_headers),
]
