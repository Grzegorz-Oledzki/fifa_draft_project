from django.shortcuts import render, redirect
from fifa_draft.forms import GroupForm, TeamForm, EditTeamForm, EditGroupForm, ChoosePersonPickingForm
from fifa_draft.models import Profile, Group, Team, Player
from fifa_draft.resources import PlayerResource
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from fifa_draft.utils import team_form_validation, edit_team_form_validation
from tablib import Dataset
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


def home(request):
    return render(request, "home.html")


@login_required(login_url="login")
def groups(request):
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, "groups.html", context)


@login_required(login_url="login")
def group(request, pk):
    group = Group.objects.get(id=pk)
    profile = request.user.profile
    context = {"group": group, "profile": profile}
    return render(request, "group.html", context)


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
            return redirect("create-team")
        else:
            messages.error(request, "Error, choose unique name or number of player from 14 to 20 are accepted.")
    context = {"form": form}
    return render(request, "group-form.html", context)


@login_required(login_url="login")
def edit_group(request, pk):
    profile = request.user.profile
    groups = Group.objects.all()
    group = profile.group_set.get(id=pk)
    form = EditGroupForm(instance=group)
    if request.method == "POST":
        form = EditGroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group edited successful!")
            return redirect("group", group.id)
        else:
            messages.error(request, "Error, choose unique name and number of player from 14 to 20 are accepted.")
    context = {"form": form, "group": group, "groups": groups}
    return render(request, "group-form.html", context)


def delete_group(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == "POST":
        group.delete()
        messages.success(request, "Group was deleted successful!")
        return redirect("home")
    context = {"group": group}
    return render(request, "delete-group.html", context)


@login_required(login_url="login")
def team(request, pk):
    profile = request.user.profile
    team = Team.objects.get(id=pk)
    players = team.team_players.all()
    context = {"team": team, "profile": profile, "players": players}
    return render(request, "team.html", context)


@login_required(login_url="login")
def create_team(request):
    form = TeamForm()
    profile = request.user.profile
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        form_valid, group_id = team_form_validation(request, form, profile)
        if form_valid:
            return redirect("group", group_id)
    context = {"form": form}
    return render(request, "team-form.html", context)


def edit_team(request, pk):
    profile = request.user.profile
    team = profile.draft_teams.get(id=pk)
    form = EditTeamForm(instance=team)
    context = {"form": form, "team": team, "profile": profile}
    if request.method == "POST":
        form = EditTeamForm(request.POST, request.FILES, instance=team)
        form_valid = edit_team_form_validation(request, form)
        if form_valid:
            return redirect("group", team.belongs_group_id)
    return render(request, "team-form.html", context)


def upload_players(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_player = request.FILES["myfile"]

        if not new_player.name.endswith('xlsx'):
            messages.error(request, 'Wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_player.read(), format='xlsx')
        for data in imported_data:
            value = Player(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                data[12],
                data[13],
                data[14],
                data[15],
                data[16],
                data[17],
                data[18],
                data[19],
                data[20],
                data[21],
                data[22],
                )
            value.save()
            return render(request, 'upload.html')


@login_required(login_url="login")
def players(request):
    profile = request.user.profile
    players = Player.objects.all()
    context = {"players": players, "profile": profile}
    return render(request, "players.html", context)


def choose_person_to_pick_players(request, pk):
    group = Group.objects.get(id=pk)
    form = ChoosePersonPickingForm(instance=group)
    if request.method == "POST":
        form = ChoosePersonPickingForm(request.POST, instance=group)
        form.save()
        return redirect('group', group.id)
    context = {'form': form}
    return render(request, "choose-picking-person.html", context)


@login_required(login_url="login")
def choose_team(request):
    profile = request.user.profile
    teams = profile.draft_teams.all()
    context = {"teams": teams, "profile": profile}
    return render(request, "choose-team.html", context)


def players_pick(request, pk):
    profile = request.user.profile
    team = Team.objects.get(id=pk)
    players = Player.objects.all()
    group = team.belongs_group
    group_players = group.group_players.all()
    picking_person = group.picking_person.all()
    context = {"team": team, "profile": profile, "players": players, 'group_players': group_players,
               'picking_person': picking_person}
    return render(request, "players-pick.html", context)


def player_pick_confirmation(request, pk, team_id):
    profile = request.user.profile
    player = Player.objects.get(sofifa_id=pk)
    team = Team.objects.get(id=team_id)
    group_players = team.belongs_group.group_players.all()
    if request.method == "POST":
        team.team_players.add(player)
        team.belongs_group.group_players.add(player)
        team.belongs_group.picking_person.clear()
        team.save()
        team.belongs_group.save()
        messages.success(request, 'Player picked!')
        return redirect('team', team.id)
    context = {"team": team, "profile": profile, 'group_players': group_players, 'player': player}
    return render(request, "player-pick-confirmation.html", context)


def draft_order(request, pk):
    group = Group.objects.get(id=pk)
    members = group.members.all()


