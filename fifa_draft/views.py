from django.shortcuts import render, redirect
from fifa_draft.forms import GroupForm, TeamForm
from fifa_draft.models import Profile, Group, Team
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def groups(request):
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'groups.html', context)


def group(request, pk):
    group = Group.objects.get(id=pk)
    context = {'group': group}
    return render(request, 'group.html', context)

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


def edit_group(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)
    if form.is_valid():
        form = GroupForm(request.POST, request.FILES, instance=group)
        if request.method == "POST":
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


def team(request, pk):
    team = Team.objects.get(id=pk)
    context = {'team': team}
    return render(request, 'team.html', context)


def create_team(request):
    form = TeamForm()
    profile = request.user.profile
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            if team.belongs_group.password == team.group_password and profile not in team.belongs_group.members.all():
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
            else:
                messages.error(request, 'Password error')
        else:
            messages.error(request, 'Please choose unique name')
    context = {'form': form}
    return render(request, 'team-form.html', context)


def edit_team(request, pk):
    profile = request.user.profile
    team = profile.draft_teams.get(id=pk)
    form = TeamForm(instance=team)
    if form.is_valid():
        form = TeamForm(request.POST, request.FILES, instance=team)
        if request.method == "POST":
            form.save()
            messages.success(request, 'Team edited successful!')
            return redirect("home")
    else:
        messages.error(request, 'Please choose unique name')
    context = {"form": form, "team": team}
    return render(request, 'team-form.html', context)
