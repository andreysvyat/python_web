from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('', views.hello_world),
    path('hello', views.hello_world),
    path("headers", views.show_headers),
    path('hello/<str:name>', views.hello_name),
    path('tasks/<int:task_id>', views.task, name='task'),
    path("tasks/<int:task_id>/select/", views.select, name='select'),
    path('task_members/<int:tm_id>/tasks', views.task_member_tasks)
]
