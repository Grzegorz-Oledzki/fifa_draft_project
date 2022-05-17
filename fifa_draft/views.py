from django.shortcuts import render, redirect
from fifa_draft.forms import GroupForm, TeamForm
from fifa_draft.models import Profile, Group, Team
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from fifa_draft.utils import team_form_validation, edit_team_form_validation



def home(request):
    return render(request, 'home.html')


@login_required(login_url="login")
def groups(request):
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'groups.html', context)


@login_required(login_url="login")
def group(request, pk):
    group = Group.objects.get(id=pk)
    profile = request.user.profile
    context = {'group': group, 'profile': profile}
    return render(request, 'group.html', context)


@login_required(login_url="login")
def create_group(request):
    form = GroupForm()
    profile = request.user.profile
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = profile
            form.save()
            messages.success(request, "Now create a team!")
            return redirect('create-team')
        else:
            messages.error(request, 'Only number of player from 14 to 20 are accepted.')
    context = {'form': form}
    return render(request, 'group-form.html', context)


@login_required(login_url="login")
def edit_group(request, pk):
    profile = request.user.profile
    group = profile.group_set.get(id=pk)
    form = GroupForm(instance=group)
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group edited successful!')
            return redirect("home")
        else:
            messages.error(request, 'Only number of player from 14 to 20 are accepted.')
    context = {"form": form, "group": group}
    return render(request, 'group-form.html', context)


def delete_group(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == "POST":
        group.delete()
        messages.success(request, 'Group was deleted successful!')
        return redirect("home")
    context = {'group': group}
    return render(request, 'delete-group.html', context)


@login_required(login_url="login")
def team(request, pk):
    profile = request.user.profile
    team = Team.objects.get(id=pk)
    context = {'team': team, 'profile': profile}
    return render(request, 'team.html', context)


@login_required(login_url="login")
def create_team(request):
    form = TeamForm()
    profile = request.user.profile
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        form_valid, group_id = team_form_validation(request, form, profile)
        if form_valid == 1:
            return redirect('group', group_id)
    context = {'form': form}
    return render(request, 'team-form.html', context)


def edit_team(request, pk):
    profile = request.user.profile
    team = profile.draft_teams.get(id=pk)
    form = TeamForm(instance=team)
    context = {"form": form, "team": team, "profile": profile}
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES, instance=team)
        form_valid = edit_team_form_validation(request, form)
        if form_valid == 1:
            return redirect('group', team.belongs_group_id)
    return render(request, 'team-form.html', context)
