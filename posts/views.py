from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like


@login_required
def home(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        image = request.FILES.get("image")
        if content:
            Post.objects.create(author=request.user, content=content, image=image)
        return redirect("home")

    posts = Post.objects.select_related("author").prefetch_related("likes", "comments")
    liked_ids = set(
        Like.objects.filter(user=request.user).values_list("post_id", flat=True)
    )
    for post in posts:
        post.liked_by_me = post.pk in liked_ids
    return render(request, "posts/home.html", {"posts": posts})


@login_required
def toggle_like(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))