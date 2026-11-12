from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Follow
from posts.models import Post


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)
    posts = Post.objects.filter(author=profile_user)
    is_following = Follow.objects.filter(
        follower=request.user, following=profile_user
    ).exists()
    return render(
        request,
        "accounts/profile.html",
        {
            "profile_user": profile_user,
            "profile": profile,
            "posts": posts,
            "is_following": is_following,
            "is_own": profile_user == request.user,
        },
    )


@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if request.method == "POST" and target != request.user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=target
        )
        if not created:
            follow.delete()
    return redirect("profile", username=username)

    

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.bio = request.POST.get("bio", "").strip()[:300]
        avatar = request.FILES.get("avatar")
        if avatar:
            profile.avatar = avatar
        profile.save()
        return redirect("profile", username=request.user.username)
    return render(request, "accounts/edit_profile.html", {"profile": profile})




@login_required
def search_users(request):
    query = request.GET.get("q", "").strip()
    users = []
    if query:
        users = User.objects.filter(username__icontains=query).select_related("profile")[:20]
    return render(request, "accounts/search.html", {"users": users, "query": query})