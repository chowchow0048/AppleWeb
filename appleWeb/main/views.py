from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.models import Board, Review


# main_home
def main(request):
    article_list = Board.objects.all().order_by("-created_at")
    paginator = Paginator(article_list, 10)

    page = request.GET.get("page")
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    # 임시: importance 컬럼이 없는 경우 created_at으로 정렬
    try:
        reviews = Review.objects.order_by("importance")
    except Exception:
        reviews = Review.objects.order_by("-created_at")

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
    article_list = Board.objects.all().order_by("created_at")
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
