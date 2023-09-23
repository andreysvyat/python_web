import django.views.defaults
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render
from django.urls import path, re_path
from django.views.static import serve

from task_tracker import settings
from . import views

urlpatterns = [
    path('autoescape', views.autoescape),
    path('comment', lambda req: HttpResponse(render(req, "comment.html"))),
    path('load', lambda req: HttpResponse(render(req, "load.html", req.GET.dict()))),
    path('repeatable', views.repeatable),
    path('filters', views.filters),
    path('server_error', django.views.defaults.server_error),
    path('raise', views.raise_ex)
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
