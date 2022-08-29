from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render

from fifa_draft.models import Profile
from users.forms import CustomUserCreationForm, ProfileForm


def login_user(request: WSGIRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)
        messages.success(request, "User logged!")

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "home")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "login_register.html")


def logout_user(request: WSGIRequest) -> HttpResponse:
    logout(request)
    messages.success(request, "User logout!")
    return redirect("login")


def register_user(request: WSGIRequest) -> HttpResponse:
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User registered!")
            login(request, user)
            return redirect("edit-account")

        else:
            messages.error(
                request, "Email error, or featured image is too big (max 3mb)"
            )

    context = {"page": page, "form": form}
    return render(request, "login_register.html", context)


def profiles(request: WSGIRequest) -> HttpResponse:
    profiles = Profile.objects.all
    context = {"profiles": profiles}
    return render(request, "profiles.html", context)


def user_profile(request: WSGIRequest, pk: str) -> HttpResponse:
    profile = Profile.objects.get(id=pk)
    context = {"profile": profile}
    return render(request, "user-profile.html", context)


def user_account(request: WSGIRequest) -> HttpResponse:
    profile = request.user.profile
    teams = profile.team_set.all()
    groups = profile.group_set.all()
    context = {"profile": profile, "teams": teams, "groups": groups}
    return render(request, "account.html", context)


def edit_account(request: WSGIRequest) -> HttpResponse:
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            messages.success(request, "User updated!")
            return redirect("account")
        else:
            messages.error(
                request, "Email error, or featured image is too big (max 3mb)"
            )
    context = {"form": form}
    return render(request, "profile_form.html", context)


def delete_account(request: WSGIRequest, pk: str) -> HttpResponse:
    profile = Profile.objects.get(id=pk)
    context = {"profile": profile}
    if request.method == "POST":
        for group in profile.group_set.all():
            group.delete()
        for team in profile.team_set.all():
            team.belongs_group.delete()
        profile.delete()
        messages.success(request, "User deleted, see you soon!")
        return redirect("home")
    return render(request, "delete_profile.html", context)
