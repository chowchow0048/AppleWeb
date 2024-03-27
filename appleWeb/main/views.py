from django.shortcuts import render
from common.models import Board


def main(req):
    boards = Board.objects.filter(posted_in="main").order_by("-created_at")[:5]
    return render(req, "main/main_home.html", {"boards": boards})


def schedule(req):
    # 'option' 파라미터로 선택한 시간표 정보를 가져옵니다.
    # 예제에서는 단순화를 위해 option 처리를 생략합니다.
    return render(req, "main/main_schedule.html")


def notice(req):
    return render(req, "main/main_notice.html")
