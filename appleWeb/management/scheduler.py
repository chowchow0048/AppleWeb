from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta, time  # time 추가
from django.db.models.functions import Extract  # Extract 함수도 상단에서 import
from common.models import Course
import logging
import signal
import sys

# 스케줄러 전용 로거 설정
logger = logging.getLogger("appleWeb.scheduler")


def signal_handler(signum, frame):
    try:
        logger.info("스케줄러를 종료합니다...")
        scheduler.shutdown(wait=False)
    except Exception as e:
        logger.error(f"종료 중 오류 발생: {str(e)}")
    finally:
        sys.exit(0)


def process_payment_deductions():
    """
    2시간 전에 시작된 수업들의 결제횟수를 차감하는 함수
    """
    try:
        # 현재 시각 기준 2시간 전 시간 계산 (KST)
        current_time = timezone.localtime(timezone.now())
        target_time = current_time - timedelta(hours=2)

        # 시와 분만 사용하여 비교
        target_hour_minute = time(target_time.hour, target_time.minute)

        # 해당 요일의 수업들 조회
        target_day = target_time.strftime("%A")
        day_mapping = {
            "Monday": "월요일",
            "Tuesday": "화요일",
            "Wednesday": "수요일",
            "Thursday": "목요일",
            "Friday": "금요일",
            "Saturday": "토요일",
            "Sunday": "일요일",
        }
        target_day_kr = day_mapping[target_day]

        logger.info(f"현재 시간(KST): {current_time.strftime('%Y-%m-%d %H:%M')}")
        logger.info(f"대상 시간(KST): {target_time.strftime('%Y-%m-%d %H:%M')}")
        logger.info(f"요일: {target_day_kr}, 시간: {target_hour_minute}")

        # 해당 요일, 시간에 진행된 수업들 조회
        courses = (
            Course.objects.filter(course_day=target_day_kr, is_active=True)
            .annotate(
                hour=Extract("course_time", "hour"),
                minute=Extract("course_time", "minute"),
            )
            .filter(hour=target_hour_minute.hour, minute=target_hour_minute.minute)
            .select_related()
        )

        if courses:
            logger.info(f"처리할 활성 수업 수: {courses.count()}")

            # 각 수업별로 수강생들의 결제횟수 차감
            processed_students = set()
            for course in courses:
                logger.info(f"처리중 수업: {course}")

                students = course.course_students.filter(is_active=True)
                logger.info(f"{course}: {students.count()}명의 활성화된 학생")

                # 배치 업데이트를 위한 리스트
                students_to_update = []

                for student in students:
                    logger.info(f"    처리중인 학생: {student}")
                    student.payment_count -= 1
                    # 결제횟수가 0 이하가 되면 결제 요청 설정
                    if student.payment_count <= 0:
                        student.payment_request = True
                        logger.info(f"    {student}의 결제가 필요합니다.")

                    students_to_update.append(student)
                    logger.info(
                        f"    {student}의 결제횟수 1회 감소. 현재 결제횟수: {student.payment_count}"
                    )
                    processed_students.add(student.id)

                # 배치 저장
                for student in students_to_update:
                    student.save()

            logger.info(f"{len(processed_students)}명의 학생 결제횟수 감소 완료.")
            return f"{len(processed_students)}명의 학생 결제횟수 감소 완료."
        else:
            logger.info("처리할 수업이 없습니다.")
            logger.info(
                f"검색 조건 - 요일: {target_day_kr}, 시간: {target_hour_minute}"
            )
            return "처리할 수업이 없습니다."

    except Exception as e:
        error_msg = f"결제횟수 감소 중 오류 발생: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise Exception(error_msg)


def start_scheduler():
    """
    스케줄러 초기화 및 작업 등록
    """
    global scheduler

    try:
        logger.info("스케줄러 초기화 중...")
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # 결제 차감 작업 등록 (1분 간격으로 테스트)
        scheduler.add_job(
            process_payment_deductions,
            "interval",
            minutes=1,
            id="process_payment_deductions",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        logger.info("결제 차감 작업이 스케줄에 등록되었습니다")

        # 시그널 핸들러 등록
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        scheduler.start()
        logger.info("스케줄러가 성공적으로 시작되었습니다")

        # 프로세스 유지를 위한 무한 루프
        try:
            while True:
                import time as time_module  # time 모듈과 구분하기 위해 별칭 사용

                time_module.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            logger.info("종료 요청... 스케줄러를 종료합니다")
            scheduler.shutdown(wait=False)
            sys.exit(0)

    except Exception as e:
        logger.error(f"스케줄러 시작 실패: {str(e)}", exc_info=True)
        raise

    return scheduler
