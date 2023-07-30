from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils.timezone import now

from .models import *

STATUSES = ['INIT', 'IN_PROGRESS', 'TEST', 'DONE']


def hello_world(request: HttpRequest):
    return HttpResponse(content='Hello world')


def show_headers(request: HttpRequest):
    headers = [f'<br>&emsp;{key}: {value}' for key, value in request.headers.items()]
    return HttpResponse(f'Hello from my first view<br>Headers in from your request: {"".join(headers)}')


def hello_name(request: HttpRequest, name: str):
    return HttpResponse(content=f'Hello {name}')


class TaskView(generic.DetailView):
    model = Task
    template_name = 'task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = STATUSES
        return context

    def get_object(self, **kwargs):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_access = now()
        obj.save()
        return obj


class TasksListView(generic.ListView):
    template_name = 'tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.all().order_by('estimate')


def member_tasks(req, tm_id):
    tm = get_object_or_404(TaskMember, pk=tm_id)
    assigned_tasks = Task.objects.filter(assigned_to=tm.id)
    return HttpResponse(render(req, 'task_member.html', {'task_member': tm, 'tasks': assigned_tasks}))


def select(req, task_id):
    t = get_object_or_404(Task, id=task_id)
    new_status = req.POST['status']
    t.status = new_status
    t.save()
    return HttpResponseRedirect(reverse('app:task_details', args=(t.id,)))
