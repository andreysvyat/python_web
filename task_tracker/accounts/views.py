import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


def login_me(request):
    if not request.POST:
        return HttpResponse(render(request, 'login.html'))
    username = request.POST["login"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('accounts:me'))
    else:
        return HttpResponse(render(request, 'login.html', {'error': 'Invalid login or password'}))


def signin(request):
    if not request.POST:
        return HttpResponse(render(request, "signin.html"))
    if not request.POST["password"] == request.POST['spass']:
        return HttpResponse(render(request, "signin.html", {'error': 'Password and submit password don\'t match'}))
    user = User.objects.create_user(
        request.POST['login'],
        request.POST['email'] if request.POST['first_name'] else None,
        request.POST['password'],
        first_name=request.POST['first_name'] if request.POST['first_name'] else None,
        last_name=request.POST['last_name'] if request.POST['last_name'] else None
    )
    user.groups.add(Group.objects.get(name='tasker'))
    user.save()
    return redirect('accounts:login')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def send_email(req):
    if req.POST:
        user: User = req.user
        email_request = req.POST.dict()
        del email_request['csrfmiddlewaretoken']
        try:
            user.email_user(**email_request)
        except Exception as e:
            logging.exception(e)
        finally:
            return HttpResponseRedirect(reverse('accounts:me'))


def _any_method_arg(req, key):
    return req.GET.get(key) if req.GET else req.POST.get(key)
