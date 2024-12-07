from django.core.management.base import BaseCommand
from management.scheduler import start_scheduler


class Command(BaseCommand):
    """
    스케줄러를 시작하기 위한 Django management 명령어
    사용법: python manage.py start_scheduler
    """

    # 명령어 도움말
    help = "Starts the APScheduler"

    def handle(self, *args, **options):
        """
        명령어가 실행될 때 호출되는 메소드
        """
        # 시작 메시지 출력
        self.stdout.write("Starting scheduler...")

        # 스케줄러 시작
        start_scheduler()

        # 성공 메시지 출력 (녹색으로 표시)
        self.stdout.write(self.style.SUCCESS("Scheduler successfully started!"))
