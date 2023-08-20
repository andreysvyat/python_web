from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('', views.TasksListView.as_view(), name='task_list'),
    path('meta', views.request_meta),
    path('play_with_response', views.play_with_response),
    path('hello', views.hello_world),
    path("headers", views.show_headers),
    path('hello/<str:name>', views.hello_name),
    path('tasks/<int:pk>', views.TaskView.as_view(), name='task_details'),
    path("tasks/<int:task_id>/change_status/", views.select, name='change_status'),
    path('task_members/<int:tm_id>', views.member_tasks, name='member_details')
]
