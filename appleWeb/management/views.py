from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from common.models import Course, User, Attendance, Absence
from django.utils import timezone
from django.db import transaction
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
import pandas as pd
import datetime
import json


@login_required
def api_students(request):
    school = request.GET.get("school")
    grade = request.GET.get("grade")
    students_query = User.objects.filter(is_active=True)  # 활성화된 사용자만 조회

    if school:
        students_query = students_query.filter(school=school)
    if grade and grade != "전체":
        students_query = students_query.filter(grade=grade)

    students_data = [
        {
            "id": student.id,
            "school": student.school,
            "grade": student.grade,
            "name": student.name,
            "phone": student.phone,
            "parent_phone": student.parent_phone,
            "payment_count": student.payment_count,
        }
        for student in students_query
    ]

    return JsonResponse(students_data, safe=False)


@login_required
def api_courses(request):
    day = request.GET.get("day")
    school = request.GET.get("school")
    courses = Course.objects.filter(course_day=day, course_school=school)
    # 시연용 일요일 수업 불러오기 코드
    # courses = Course.objects.filter(course_day="일요일", course_school=school)

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


@login_required
@csrf_exempt
def record_attendance(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student_id = data.get("student_id")
            course_id = data.get("course_id")

            with transaction.atomic():  # Ensure the atomicity of the transaction
                student = User.objects.select_for_update().get(id=student_id)
                course = Course.objects.get(id=course_id)

                # Update payment count and request
                student.payment_count -= 1
                if student.payment_count == 0:
                    student.payment_request = True
                student.save()

                # Create attendance record
                Attendance.objects.create(
                    student=student, course=course, date=timezone.now().date()
                )

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Attendance recorded and payment count updated.",
                }
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )
        except User.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Student not found"}, status=404
            )
        except Course.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Course not found"}, status=404
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid request"}, status=400
        )


@login_required
@require_POST
def record_absence(request):
    try:
        data = json.loads(request.body)
        student_id = data["student_id"]
        course_id = data["course_id"]

        with transaction.atomic():
            student = get_object_or_404(User, pk=student_id)
            course = get_object_or_404(Course, pk=course_id)
            Absence.objects.create(
                student=student, course=course, date=timezone.now().date()
            )

        return JsonResponse({"status": "success", "message": "결석이 기록되었습니다."})
    except json.JSONDecodeError as e:
        return JsonResponse(
            {"status": "error", "message": "잘못된 JSON 형식입니다: " + str(e)},
            status=400,
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
def export_attendance_to_excel(request, course_id):
    course = Course.objects.get(id=course_id)
    students = course.course_students.all()  # 코스에 등록된 모든 학생들을 불러옴

    # 엑셀 파일 제목 줄 설정
    today = timezone.now().strftime("%Y-%m-%d")
    subject = course.course_subject.capitalize()  # 과목명을 적절히 포맷팅
    title = f"{course.course_school} {course.course_grade} {subject} / {course.course_day} {course.course_time.strftime('%H:%M')} / {today}"

    # 워크북 생성
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"
    ws.append(["학교", "학년", "이름", "전화번호", "부모님 전화번호", "출석", "결석"])

    # 학생 데이터 추가
    for student in students:
        ws.append(
            [
                student.school,
                student.grade,
                student.name,
                student.phone if student.phone else "-",
                student.parent_phone if student.parent_phone else "-",
                "",  # 출석
                "",  # 결석
            ]
        )

    # 열 너비 조정
    for col in range(1, 8):  # 열 A부터 G까지
        ws.column_dimensions[get_column_letter(col)].width = 20

    # 제목 행 병합 및 스타일 설정
    ws.insert_rows(1)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=7)
    ws.cell(row=1, column=1).value = title
    ws.cell(row=1, column=1).alignment = Alignment(horizontal="center")

    # HTTP 응답 설정
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{title}.xlsx"'

    # 엑셀 파일 저장 및 전송
    wb.save(response)
    return response


@login_required
@require_POST
def confirm_payment(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.grade == "1학년":
        user.payment_count += 4
    else:
        user.payment_count += 12
    user.payment_request = False
    user.save()

    return JsonResponse(
        {
            "message": "Payment confirmed successfully",
            "payment_count": user.payment_count,
        }
    )


@login_required
def management_home(request):
    return render(request, "management/management_home.html")


@login_required
def management_studentlist(request):
    return render(request, "management/management_studentlist.html")


@login_required
def management_studentlist_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    students = course.course_students.all()
    today = timezone.now().date()

    print("STUDENTLIST DETAIL-------")
    print("course:", course)
    print("students:", students)
    print("course_id:", course_id)
    print("today:", today)

    attendance_records = {
        attendance.student.id: attendance
        for attendance in Attendance.objects.filter(course=course, date=today)
    }

    absence_records = {
        absence.student.id: absence
        for absence in Absence.objects.filter(course=course, date=today)
    }

    print("STUDENTLIST DETAIL END-------")
    return render(
        request,
        "management/management_studentlist_detail.html",
        {
            "course": course,
            "students": students,
            "attendance_records": attendance_records,
            "absence_records": absence_records,
        },
    )


@login_required
@require_POST  # 이 뷰 함수는 POST 요청만 허용
def bulk_attendance(request):
    date = timezone.now().date()  # 오늘 날짜를 가져옴
    course_id = request.POST.get("course_id")  # POST 데이터에서 course_id를 가져옴

    # print("BULK ATTENDANCE-------0------")
    # print("course_id:", course_id, "date:", date)
    # print(
    #     "attendance_ids:", request.POST.getlist("attendance")
    # )  # POST 데이터에서 attendance 리스트를 가져옴
    # print(
    #     "absence_ids:", request.POST.getlist("absence")
    # )  # POST 데이터에서 absence 리스트를 가져옴
    # print("BULK ATTENDANCE ENDENDENDENEND-------0------")

    if not course_id:
        return redirect("management_home")  # course_id가 없으면 홈 페이지로 리디렉션

    course = get_object_or_404(
        Course, id=course_id
    )  # 주어진 course_id에 해당하는 Course 객체를 가져옴

    attendance_ids = request.POST.getlist(
        "attendance"
    )  # POST 데이터에서 attendance 리스트를 가져옴
    absence_ids = request.POST.getlist(
        "absence"
    )  # POST 데이터에서 absence 리스트를 가져옴

    # 해당 course, date가 일치하는 출석 및 결석 기록을 초기화.
    Attendance.objects.filter(
        course=course, date=date
    ).delete()  # 해당 날짜와 Course에 대한 기존 출석 기록을 삭제
    Absence.objects.filter(
        course=course, date=date
    ).delete()  # 해당 날짜와 Course에 대한 기존 결석 기록을 삭제

    # Record new attendance
    for student_id in attendance_ids:
        student = course.course_students.get(
            id=student_id
        )  # student_id에 해당하는 학생을 가져옴
        Attendance.objects.create(
            course=course, student=student, date=date
        )  # 새로운 출석 기록을 생성

    # Record new absence
    for student_id in absence_ids:
        student = course.course_students.get(
            id=student_id
        )  # student_id에 해당하는 학생을 가져옴
        Absence.objects.create(
            course=course, student=student, date=date
        )  # 새로운 결석 기록을 생성

    return redirect(
        "management_studentlist_detail", course_id=course_id
    )  # 출석부 페이지로 리디렉션

    return redirect("management_home")  # 기본 리디렉션


# @login_required
# def bulk_attendance(request):
#     if request.method == "POST":
#         date = timezone.now().date()
#         # date = '일요일'
#         course_id = request.POST.get("course_id")

#         print("BULK ATTENDANCE-------0------")
#         print("course_id:", course_id, "date:", date)
#         print("attendance_ids:", request.POST.getlist("attendance"))
#         print("absence_ids:", request.POST.getlist("absence"))
#         print("BULK ATTENDANCE ENDENDENDENEND-------0------")

#         if not course_id:
#             return redirect("management_home")

#         course = get_object_or_404(Course, id=course_id)

#         attendance_ids = request.POST.getlist("attendance")
#         absence_ids = request.POST.getlist("absence")

#         # Clear previous records for the selected date and course
#         Attendance.objects.filter(course=course, date=date).delete()
#         Absence.objects.filter(course=course, date=date).delete()

#         # Record new attendance
#         for student_id in attendance_ids:
#             student = course.course_students.get(id=student_id)
#             Attendance.objects.create(course=course, student=student, date=date)

#         # Record new absence
#         for student_id in absence_ids:
#             student = course.course_students.get(id=student_id)
#             Absence.objects.create(course=course, student=student, date=date)

#         return redirect("management_studentlist_detail", course_id=course_id)

#     return redirect("management_home")


# @login_required
# def management_studentlist_detail(request, course_id):
#     course = Course.objects.get(id=course_id)
#     students = course.course_students.all()
#     today = timezone.now().date()
#     # 각 학생별로 출석체크 여부를 확인
#     attendance_records = {
#         attendance.student.id: attendance
#         for attendance in Attendance.objects.filter(course=course, date=today)
#     }
#     absence_records = {
#         absence.student.id: absence
#         for absence in Absence.objects.filter(course=course, date=today)
#     }
#     return render(
#         request,
#         "management/management_studentlist_detail.html",
#         {
#             "course": course,
#             "students": students,
#             "attendance_records": attendance_records,
#             "absence_records": absence_records,
#         },
#     )


@login_required
def management_student_detail(request, student_id):
    student = get_object_or_404(User, pk=student_id)
    attendances = Attendance.objects.filter(student=student).order_by("attended_at")
    absences = Absence.objects.filter(student=student).order_by("absent_at")
    courses = student.enrolled_courses.all()

    context = {
        "student": student,
        "attendances": attendances,
        "absences": absences,
        "courses": courses,
    }
    return render(request, "management/management_student_detail.html", context)


@login_required
def management_paylist(request):
    users_with_payment_request = User.objects.filter(payment_request=True)
    users_with_payment_request = [
        {
            "id": user.id,
            "school": user.school,
            "grade": user.grade,
            "name": user.name,
            "phone": user.phone,
            "parent_phone": user.parent_phone,
            "payment_count": abs(user.payment_count),
        }
        for user in users_with_payment_request
    ]

    return render(
        request,
        "management/management_paylist.html",
        {"users": users_with_payment_request},
    )


# Not neccessary
# def management_notice(request):
#     return render(request, "management/management_notice.html")


@login_required
def management_waitList(request):
    return render(request, "management/management_waitlist.html")


@login_required
def management_blacklist(request):
    return render(request, "management/management_blacklist.html")
