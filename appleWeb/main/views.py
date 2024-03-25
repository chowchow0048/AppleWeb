from django.shortcuts import render


def main(req):
    return render(req, "main/main.html")


def schedule(req):
    # 'option' 파라미터로 선택한 시간표 정보를 가져옵니다.
    # 예제에서는 단순화를 위해 option 처리를 생략합니다.
    return render(req, "main/schedule.html")


def notice(req):
    return render(req, "main/notice.html")
