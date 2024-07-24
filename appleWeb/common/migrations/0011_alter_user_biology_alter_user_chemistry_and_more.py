# Generated by Django 5.0.2 on 2024-05-08 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_alter_user_grade_alter_user_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='biology',
            field=models.BooleanField(default=False, null=True, verbose_name='생명과학'),
        ),
        migrations.AlterField(
            model_name='user',
            name='chemistry',
            field=models.BooleanField(default=False, null=True, verbose_name='화학'),
        ),
        migrations.AlterField(
            model_name='user',
            name='earth_science',
            field=models.BooleanField(default=False, null=True, verbose_name='지구과학'),
        ),
        migrations.AlterField(
            model_name='user',
            name='integrated_science',
            field=models.BooleanField(default=False, null=True, verbose_name='통합과학'),
        ),
        migrations.AlterField(
            model_name='user',
            name='physics',
            field=models.BooleanField(default=False, null=True, verbose_name='물리'),
        ),
    ]
