from django import template
import datetime

register = template.Library()


@register.filter
def subject_kor(subject):
    subject_dict = {
        "earth_science": "지구과학",
        "physics": "물리",
        "chemistry": "화학",
        "biology": "생명과학",
        "integrated_science": "통합과학",
    }
    return subject_dict.get(subject, subject)


@register.filter
def time_kor(time):
    time_str = time.strftime("%I %p").lower()
    time_dict = {
        "a.m.": "오전",
        "am": "오전",
        "p.m.": "오후",
        "pm": "오후",
    }
    hour, period = time_str.split()
    hour = int(hour)
    if period == "p.m." and hour != 12:
        hour += 12
    # return f"{time_str.split()}"
    return f"{time_dict[period]} {hour}시"


@register.filter
def date_kor(date):
    return date.strftime("%Y-%m-%d")


@register.filter
def course_kor(course):
    course_school = course.course_school
    course_grade = course.course_grade
    course_subject = subject_kor(course.course_subject)
    return f"{course_school} {course_grade} {course_subject}"
