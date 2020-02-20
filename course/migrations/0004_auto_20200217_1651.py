# Generated by Django 2.2 on 2020-02-17 16:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20200217_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='assignments',
            field=models.ManyToManyField(blank=True, related_name='course_assignment', to='assignment.Assignment'),
        ),
        migrations.AlterField(
            model_name='course',
            name='assistants',
            field=models.ManyToManyField(blank=True, related_name='course_assistants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='course_participants', to=settings.AUTH_USER_MODEL),
        ),
    ]
