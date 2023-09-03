from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission, User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView


class UserView(LoginRequiredMixin, CreateView):
    template_name = 'user.html'
    login_url = 'accounts:login'

    @staticmethod
    def get_context(user: User):
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

    def get(self, request, *args, **kwargs):
        return HttpResponse(render(request, "user.html", self.get_context(request.user)))

    def post(self, request, *args, **kwargs):
        user: User = request.user
        user_dto = self.get_context(request.user)
        post = request.POST.dict()
        if 'perm' in post:
            perm = post['perm']
            user_dto['has_permission'] = user.has_perm(perm)
            user_dto['permission'] = Permission.objects.get(codename=perm).name
            return HttpResponse(render(request, "user.html", user_dto))
        if 'password' in post:
            password = post['password']
            user_dto["is_pass_valid"] = user.check_password(password)
            return HttpResponse(render(request, "user.html", user_dto))
        if 'new_password' in post:
            password = post['new_password']
            user.set_password(password)
            user.save()
            return redirect('accounts:logout')
        user_dto['errors'] = ["Not available action was called"]
        return HttpResponse(render(request, "user.html", user_dto))
