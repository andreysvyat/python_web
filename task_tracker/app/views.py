from django.http import HttpResponse, HttpRequest

from .models import *


def hello_world(request: HttpRequest):
    return HttpResponse(content='Hello world')


def hello_name(request: HttpRequest, name: str):
    return HttpResponse(content=f'Hello {name}')


def task(reqeust, task_id):
    t = Task.objects.get(id=task_id)
    return HttpResponse(f'Task {t.id} for {t.assigned_to.user_id.username}'
                        f'<br>name: {t.name} '
                        f'<br>description: {t.description}'
                        f'<br>estimated to {t.estimate}')


def task_member_tasks(req, tm_id):
    tm = TaskMember.objects.get(pk=tm_id)
    created_tasks = Task.objects.filter(created_by=tm.id)
    assigned_tasks = Task.objects.filter(assigned_to=tm.id)
    return HttpResponse(f'Tasks for {tm.user_id.username}'
                        f'<br>&emsp;Assigned {"<br>&emsp;&emsp;".join([str(t) for t in assigned_tasks])}'
                        f'<br>&emsp;Created {"<br>&emsp;&emsp;".join([str(t) for t in created_tasks])}')


def show_headers(request: HttpRequest):
    headers = [f'<br>&emsp;{key}: {value}' for key, value in request.headers.items()]
    return HttpResponse(f'Hello from my first view<br>Headers in from your request: {"".join(headers)}')
