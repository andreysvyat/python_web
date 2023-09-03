from django.urls import path

from . import views, user_view

app_name = "accounts"
urlpatterns = [
    path("signin", views.signin, name='signin'),
    path("login", views.login_me, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("me", user_view.UserView.as_view(), name="me"),
    path("email", views.send_email, name='email')
]
