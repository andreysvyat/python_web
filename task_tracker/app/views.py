from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .models import *


def hello_world(request: HttpRequest):
    return HttpResponse(content='Hello world')


def hello_name(request: HttpRequest, name: str):
    return HttpResponse(content=f'Hello {name}')


def task(reqeust, task_id):
    t = Task.objects.get(id=task_id)
    return HttpResponse(render(reqeust, 'task.html', {'task': t}))


def task_member_tasks(req, tm_id):
    tm = TaskMember.objects.get(pk=tm_id)
    assigned_tasks = Task.objects.filter(assigned_to=tm.id)
    return HttpResponse(render(req, 'task_member.html', {'task_member': tm, 'tasks': assigned_tasks}))


def show_headers(request: HttpRequest):
    headers = [f'<br>&emsp;{key}: {value}' for key, value in request.headers.items()]
    return HttpResponse(f'Hello from my first view<br>Headers in from your request: {"".join(headers)}')
