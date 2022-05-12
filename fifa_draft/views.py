from django.shortcuts import render, redirect
from fifa_draft.forms import GroupForm, TeamForm
from fifa_draft.models import Profile, Group, Team
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory



def home(request):
    return render(request, 'home.html')


def groups(request):
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'groups.html', context)


def group(request, pk):
    group = Group.objects.get(id=pk)
    profile = request.user.profile
    context = {'group': group, 'profile': profile}
    return render(request, 'group.html', context)


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
            print(form.errors)
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


def team(request, pk):
    profile = request.user.profile
    team = Team.objects.get(id=pk)
    context = {'team': team, 'profile': profile}
    return render(request, 'team.html', context)


def create_team(request):
    form = TeamForm()
    profile = request.user.profile
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            unique_name = True
            for team_name in team.belongs_group.teams.all():
                if str(team_name) == str(team):
                    unique_name = False
            if team.belongs_group.password == team.group_password and profile not in team.belongs_group.members.all() and unique_name:
                team.owner = profile
                team.max_players = team.belongs_group.number_of_players
                team.save()
                team.belongs_group.members.add(profile)
                team.draft_teams.add(profile)
                team.belongs_group.teams.add(team)
                messages.success(request, 'Team created and added to group successful!')
                return redirect('home')
            elif profile in team.belongs_group.members.all():
                messages.error(request, 'You have already team in this group')
            elif team.belongs_group.password != team.group_password:
                messages.error(request, 'Password error')
            elif not unique_name:
                messages.error(request, 'Please choose unique name')
    context = {'form': form}
    return render(request, 'team-form.html', context)


def edit_team(request, pk):
    profile = request.user.profile
    team = profile.draft_teams.get(id=pk)
    form = TeamForm(instance=team)
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team edited successful!')
            return redirect("home")
    else:
        messages.error(request, 'Please choose unique name')
    context = {"form": form, "team": team, "profile": profile}
    return render(request, 'team-form.html', context)
