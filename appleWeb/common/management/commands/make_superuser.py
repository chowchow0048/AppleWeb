from django.core.management.base import BaseCommand
from common.models import User


class Command(BaseCommand):
    help = "기존 사용자를 superuser로 변경"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="superuser로 변경할 사용자명")

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        try:
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'사용자 "{username}"가 superuser로 변경되었습니다.')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'사용자 "{username}"를 찾을 수 없습니다.')
            )
