from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.models import Board, Review


# main_home
def main(request):
    article_list = Board.objects.all()
    paginator = Paginator(article_list, 10)

    page = request.GET.get("page")
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    reviews = Review.objects.all()

    return render(
        request,
        "main/main_home.html",
        {
            "articles": articles,
            "reviews": reviews,
        },
    )


# main_home의 공지사항
def notice_data(request):
    article_list = Board.objects.all().order_by("-created_at")
    paginator = Paginator(article_list, 15)

    page = request.GET.get("page", 1)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, "partials/notice_section.html", {"articles": articles})


# main_notice_detail, 공지사항 글 자세히 보기
def notice_detail(request, id):
    article = get_object_or_404(Board, pk=id)
    return render(request, "main/main_notice_detail.html", {"article": article})


# main_review_deetail, 수강후기 자세히 보기
def review_detail(request, id):
    review = get_object_or_404(Review, pk=id)
    return render(request, "main/main_review_detail.html", {"review": review})


# def notice(request):
#     articles = Board.objects.all()
#     return render(request, "main/main_notice.html", {"articles": articles})


# from django.http import JsonResponse
# from django.contrib.auth import authenticate, login
# from common.forms import SignUpForm

# def ajax_login(request):
#     username = request.POST.get("username")
#     password = request.POST.get("password")
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return JsonResponse({"success": True})
#     else:
#         return JsonResponse({"success": False, "error": "Authentication failed"})

# def signup_view(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # 적절한 리다이렉트 또는 추가 로직 처리
#             return redirect("main")
#     else:
#         form = SignUpForm()

#     return render(request, "main/signup.html", {"form": form})
