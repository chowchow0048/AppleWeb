# Generated by Django 5.0.2 on 2024-07-09 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0020_alter_course_course_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='활성화'),
        ),
    ]
