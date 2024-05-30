# Generated by Django 5.0.2 on 2024-05-03 17:11

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_remove_user_subjects_remove_course_course_subjects_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='parent_name',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='attended_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='출석 일시'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.course', verbose_name='수업'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to=settings.AUTH_USER_MODEL, verbose_name='학생'),
        ),
        migrations.AlterField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='enrolled_students', to='common.course', verbose_name='수업 시간표'),
        ),
        migrations.AlterField(
            model_name='user',
            name='grade',
            field=models.CharField(blank=True, choices=[('1학년', '1학년'), ('2학년', '2학년'), ('3학년', '3학년')], max_length=10, null=True, verbose_name='학년'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='활성화'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_manager',
            field=models.BooleanField(default=False, verbose_name='행정'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(default=False, verbose_name='강사'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, verbose_name='이름'),
        ),
        migrations.AlterField(
            model_name='user',
            name='parent_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='부모님 핸드폰 번호'),
        ),
        migrations.AlterField(
            model_name='user',
            name='payment_count',
            field=models.IntegerField(default=12, verbose_name='결제 횟수'),
        ),
        migrations.AlterField(
            model_name='user',
            name='payment_request',
            field=models.BooleanField(default=False, verbose_name='결제 요청'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='핸드폰 번호'),
        ),
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.CharField(blank=True, choices=[('세화고', '세화고'), ('세화여고', '세화여고'), ('연합반', '연합반')], max_length=50, null=True, verbose_name='학교'),
        ),
    ]