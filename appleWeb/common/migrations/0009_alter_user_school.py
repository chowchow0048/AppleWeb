# Generated by Django 5.0.2 on 2024-05-04 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_alter_course_course_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.CharField(blank=True, choices=[('세화고', '세화고'), ('세화여고', '세화여고'), ('연합반', '연합반')], max_length=50, verbose_name='학교'),
        ),
    ]
