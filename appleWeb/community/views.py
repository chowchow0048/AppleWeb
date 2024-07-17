from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from common.models import Course


@never_cache
@login_required
def community_home(req):
    return render(req, "community/community_home.html")


@login_required
def community_notice(req):
    return render(req, "community/community_notice.html")


@login_required
def api_courses(request):
    day = request.GET.get("day")
    school = request.GET.get("school")
    courses = Course.objects.filter(
        course_day=day, course_school=school, is_active=True
    )

    # Testing: 일요일 수업만
    # courses = Course.objects.filter(
    #     course_day="일요일", course_school=school, is_active=True
    # )

    # print("VIEWS - COMMUNITY COURSES:", courses)

    data = [
        {
            "id": course.id,
            "course_grade": course.course_grade,
            "course_subject": course.course_subject,  # 직접 과목 이름을 사용
            "course_time": course.course_time.strftime("%H:%M"),
        }
        for course in courses
    ]
    return JsonResponse(data, safe=False)
