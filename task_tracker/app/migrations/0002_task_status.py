# Generated by Django 4.2.3 on 2023-07-27 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(default='INIT', max_length=63),
        ),
    ]
