from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.timezone import now
from django.views import generic

from .models import *

STATUSES = ['INIT', 'IN_PROGRESS', 'TEST', 'DONE']


# noinspection PyUnusedLocal
def hello_world(request: HttpRequest):
    print("Do some staff")
    return HttpResponse(content="Hello world")


def show_headers(request: HttpRequest):
    return HttpResponse(f'Hello from my first view<br>Headers in from your request: {request.headers}')


def __headers_to_string(headers):
    headers = [f'<br>&emsp;{key}: {value}' for key, value in headers.items()]
    return f'{"".join(headers)}'


def request_meta(req: HttpRequest):
    c = f'Scheme: {req.scheme}<br>' \
        f'Path: {req.path}<br>' \
        f'Method: {req.method}<br>' \
        f'Encoding: {req.encoding}<br>' \
        f'Content-Type: {req.content_type}<br>' \
        f'Get query as dictionary: {req.GET.dict()}<br>' \
        f'Cookies: {req.COOKIES}<br>' \
        f'META or headers: {__headers_to_string(req.headers)}<br>' \
        f'Methods:' \
        f'<br>&emsp;get_full_path(): {req.get_full_path()}' \
        f'<br>&emsp;get_host(): {req.get_host()}' \
        f'<br>&emsp;get_port(): {req.get_port()}'
    return HttpResponse(content=c)


def play_with_response(req: HttpRequest):
    content = req.GET.get('content')
    headers = {str(h).split(':')[0]: str(h).split(':')[1] for h in req.GET.getlist('headers')}
    charset = req.GET.get('charset', None)
    status = int(req.GET.get('status', 200))
    reason = req.GET.get('reason', None)
    content_type = req.GET.get('type', None)
    return HttpResponse(content, content_type, status, reason, charset, headers)


def hello_name(request: HttpRequest, name: str):
    if request.GET.get('surname'):
        return HttpResponse(content=f'Hello {name.capitalize()} {request.GET.get("surname")}')
    return HttpResponse(content=f'Hello {name.capitalize()}')


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
