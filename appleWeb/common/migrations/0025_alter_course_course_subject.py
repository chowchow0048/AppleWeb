# Generated by Django 5.0.2 on 2024-08-31 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0024_alter_course_course_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_subject',
            field=models.CharField(choices=[('physics', '물리'), ('chemistry', '화학'), ('biology', '생명과학'), ('earth_science', '지구과학'), ('integrated_science', '통합과학')], default='선택과목', max_length=30, verbose_name='선택과목'),
        ),
    ]