from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post


@login_required
def home(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        image = request.FILES.get("image")
        if content:
            Post.objects.create(author=request.user, content=content, image=image)
        return redirect("home")

    posts = Post.objects.select_related("author").prefetch_related("likes", "comments")
    return render(request, "posts/home.html", {"posts": posts})