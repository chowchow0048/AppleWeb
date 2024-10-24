# Generated by Django 5.0.2 on 2024-08-05 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0021_course_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='review_images/', verbose_name='이미지'),
        ),
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(max_length=3000, verbose_name='수강 후기'),
        ),
    ]
