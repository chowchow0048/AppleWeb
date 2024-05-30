# Generated by Django 5.0.2 on 2024-05-12 18:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0014_course_course_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attended_student', to=settings.AUTH_USER_MODEL, verbose_name='학생'),
        ),
        migrations.AlterField(
            model_name='user',
            name='attended_dates',
            field=models.ManyToManyField(blank=True, related_name='attended_at', to='common.attendance', verbose_name='출석 날짜'),
        ),
        migrations.CreateModel(
            name='Absent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='결석 날짜')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='absent', to='common.course', verbose_name='수업')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='absent_student', to=settings.AUTH_USER_MODEL, verbose_name='학생')),
            ],
            options={
                'verbose_name': '결석',
                'verbose_name_plural': '결석',
                'ordering': ['date'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='absent_dates',
            field=models.ManyToManyField(blank=True, related_name='absent_at', to='common.absent', verbose_name='결석 날짜'),
        ),
    ]
