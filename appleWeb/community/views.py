from django.shortcuts import render


# Create your views here.
def community(req):
    return render(req, "community/community_main.html")
