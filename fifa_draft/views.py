from django.shortcuts import render, redirect
from fifa_draft.forms import GroupForm, TeamForm
from fifa_draft.models import Profile, Group, Team
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def create_group(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Now create a team!")
            return redirect('home')
        else:
            messages.error(request, 'Only number of player from 14 to 20 are accepted.')
    context = {'form': form}
    return render(request, 'group-form.html', context)


def create_team(request):
    form = TeamForm()
    profile = request.user.profile
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            if team.belongs_group.password == team.group_password:
                team.owner = profile
                team.max_players = team.belongs_group.number_of_players
                team.save()
                team.belongs_group.members.add(profile)
                team.draft_teams.add(profile)
                team.belongs_group.teams.add(team)
                return redirect('home')
            else:
                messages.error(request, 'Password error')
    context = {'form': form}
    return render(request, 'team-form.html', context)
