from django.db import models
from django.contrib.auth.models import User


class TaskMember(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    position = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f'{self.user_id} {self.position}'


class Task(models.Model):
    created_by = models.ForeignKey(TaskMember, on_delete=models.DO_NOTHING, related_name='created_by')
    assigned_to = models.ForeignKey(TaskMember, on_delete=models.DO_NOTHING, related_name='assigned_to')
    status = models.CharField(max_length=63, default='INIT')
    created = models.DateTimeField("date published")
    estimate = models.IntegerField('Estimate in hours', default=8)
    name = models.CharField(max_length=511)
    description = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return f'{self.id} {self.name} {self.description}'
