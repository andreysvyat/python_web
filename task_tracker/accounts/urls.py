from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("signin", views.signin, name='signin'),
    path("login", views.login_me, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("me", views.me, name="me"),
    path("me/pass", views.check_password, name="check_pass"),
    path("me/perms", views.has_permission, name="has_perm"),
    path('me/upd_path', views.upd_password, name='upd_pass'),
    path("email", views.send_email, name='email')
]
