from django.http import HttpResponse, HttpRequest, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import *


def hello_world(request: HttpRequest):
    return HttpResponse(content='Hello world')


def show_headers(request: HttpRequest):
    headers = [f'<br>&emsp;{key}: {value}' for key, value in request.headers.items()]
    return HttpResponse(f'Hello from my first view<br>Headers in from your request: {"".join(headers)}')


def hello_name(request: HttpRequest, name: str):
    return HttpResponse(content=f'Hello {name}')


def task(reqeust, task_id):
    try:
        t = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404('Task member not found')
    return HttpResponse(render(reqeust, 'task.html', {'task': t, 'statuses': statuses()}))


def task_member_tasks(req, tm_id):
    tm = get_object_or_404(TaskMember, pk=tm_id)
    assigned_tasks = Task.objects.filter(assigned_to=tm.id)
    return HttpResponse(render(req, 'task_member.html', {'task_member': tm, 'tasks': assigned_tasks}))


def statuses():
    return ['INIT', 'IN_PROGRESS', 'TEST', 'DONE']


def select(req, task_id):
    t = get_object_or_404(Task, id=task_id)
    new_status = req.POST['status']
    t.status = new_status
    t.save()
    return HttpResponseRedirect(reverse('app:task', args=(t.id,)))
