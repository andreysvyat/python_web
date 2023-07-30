from django.urls import path

from . import views

urlpatterns = [
    path('', views.hello_world),
    path('hello', views.hello_world),
    path("headers", views.show_headers),
    path('hello/<str:name>', views.hello_name),
    path('tasks/<int:task_id>', views.task, name='task'),
    path('task_members/<int:tm_id>/tasks', views.task_member_tasks)
]
