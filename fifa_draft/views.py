from django.shortcuts import render, redirect
from fifa_draft.forms import GroupForm
from fifa_draft.models import Profile, Group
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def create_group(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, 'Only number of player from 14 to 20 are accepted.')
    context = {'form': form}
    return render(request, 'group-form.html', context)
