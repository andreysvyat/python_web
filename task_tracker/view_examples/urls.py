from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

from . import views

urlpatterns = [
    path('autoescape', views.autoescape),
    path('comment', lambda req: HttpResponse(render(req, "comment.html"))),
    path('load', lambda req: HttpResponse(render(req, "load.html", req.GET.dict()))),
    path('repeatable', views.repeatable),
    path('filters', views.filters)
]
