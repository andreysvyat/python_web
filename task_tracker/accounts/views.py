import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
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
    post = request.POST.dict()
    del post['spass']
    User.objects.create_user(**post)
    return


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def me(req):
    return HttpResponse(render(req, "user.html", _get_user_dto(req.user)))


@login_required(login_url='accounts:login')
def has_permission(req):
    perm = _any_method_arg(req, 'perm')
    user: User = req.user
    user_dto = _get_user_dto(req.user)
    user_dto.update({"has_permission": user.has_perm(perm),
                     'permission': Permission.objects.get(codename=perm).name
                     })
    return HttpResponse(render(req, "user.html", user_dto))


@login_required(login_url='accounts:login')
def check_password(req):
    password = _any_method_arg(req, 'password')
    user: User = req.user
    user_dto = _get_user_dto(req.user)
    user_dto.update({"is_pass_valid": user.check_password(password)})
    return HttpResponse(render(req, "user.html", user_dto))


@login_required(login_url='accounts:login')
def upd_password(req):
    password = _any_method_arg(req, 'password')
    user: User = req.user
    user.set_password(password)
    user.save()
    return redirect('accounts:logout')


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


def _get_user_dto(user: User):
    return {
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "login": user.username,
            "last_login": user.last_login,
            "created": user.date_joined,
            "is_active": user.is_active,
            "is_admin": user.is_staff,
            "is_authenticated": user.is_authenticated,
            "is_anonim": user.is_anonymous,
            "is_super_user": user.is_active,
            "full_name": user.get_full_name(),
            "short_name": user.get_short_name(),
            "groups": [group.name for group in user.groups.all()],
            "permissions": user.get_user_permissions()
        },
        "all_perms": [{"name": permission.name, "code": permission.codename} for permission in
                      Permission.objects.all()]
    }
