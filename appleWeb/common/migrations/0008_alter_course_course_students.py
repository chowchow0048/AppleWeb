# Generated by Django 5.0.2 on 2024-05-04 11:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_remove_user_parent_name_alter_attendance_attended_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_students',
            field=models.ManyToManyField(blank=True, null=True, related_name='enrolled_courses', to=settings.AUTH_USER_MODEL, verbose_name='학생'),
        ),
    ]
