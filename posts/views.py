from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Follow
from .models import Post, Like, Comment


@login_required
def home(request):
    posts = Post.objects.select_related("author", "author__profile").prefetch_related(
        "likes", "comments", "comments__author"
    )

    following_ids = list(
        Follow.objects.filter(follower=request.user).values_list(
            "following_id", flat=True
        )
    )
    if following_ids:
        following_ids.append(request.user.pk)
        posts = posts.filter(author_id__in=following_ids)

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


@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        text = request.POST.get("text", "").strip()
        if text:
            Comment.objects.create(post=post, author=request.user, text=text[:300])
    return redirect("home")




@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))




@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        image = request.FILES.get("image")
        if content:
            Post.objects.create(author=request.user, content=content, image=image)
            return redirect("home")
    return render(request, "posts/create.html")