from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from fifa_draft.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



def profiles(request):
    profiles = Profile.objects.all
    context = {'profiles': profiles}
    return render(request, 'profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {"profile": profile}
    return render(request, 'user-profile.html', context)
