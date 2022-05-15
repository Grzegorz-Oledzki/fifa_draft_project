from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from fifa_draft.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.forms import CustomUserCreationForm


def login_user(request):
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

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "home")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "login_register.html")


def logout_user(request):
    logout(request)
    messages.success(request, "User logout!")
    return redirect("login")


def register_user(request):
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
            #return redirect("edit-account")

        else:
            messages.error(request, "Error! User not registered")

    context = {"page": page, "form": form}
    return render(request, "login_register.html", context)

@login_required(login_url="login")
def profiles(request):
    profiles = Profile.objects.all
    context = {'profiles': profiles}
    return render(request, 'profiles.html', context)

@login_required(login_url="login")
def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {"profile": profile}
    return render(request, 'user-profile.html', context)
