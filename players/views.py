from django.shortcuts import render, redirect
from fifa_draft.models import Team
from players.models import Player
from players.utils import (
    change_picking_person,
    add_player_to_team_and_group,
    pending_player_pick,
    last_and_first_picking_persons,
)
from django.contrib.auth.decorators import login_required
from fifa_draft.utils import pick_alert
from django.contrib import messages


def upload_players(request):
    if request.method == "POST":
        dataset = Dataset()
        new_player = request.FILES["myfile"]

        if not new_player.name.endswith("xlsx"):
            messages.error(request, "Wrong format")
            return render(request, "upload.html")

        imported_data = dataset.load(new_player.read(), format="xlsx")
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
            return render(request, "upload.html")


@login_required(login_url="login")
def players(request):
    profile = request.user.profile
    players = Player.objects.all()
    context = {"players": players, "profile": profile}
    pick_alert(request, context)
    return render(request, "players.html", context)


@login_required(login_url="login")
def choose_team(request):
    profile = request.user.profile
    teams = profile.draft_teams.all()
    context = {"teams": teams, "profile": profile}
    pick_alert(request, context)
    return render(request, "choose-team.html", context)


def players_pick(request, pk):
    profile = request.user.profile
    team = Team.objects.get(id=pk)
    players = Player.objects.all()
    group = team.belongs_group
    group_players = group.group_players.all()
    picking_person = group.picking_person.all()
    context = {
        "team": team,
        "profile": profile,
        "players": players,
        "group_players": group_players,
        "picking_person": picking_person,
    }
    if team.belongs_group.draft_order:
        first_person, last_person = last_and_first_picking_persons(team)
        context["last_team"] = last_person
        context["first_person"] = first_person

    pick_alert(request, context)
    return render(request, "players-pick.html", context)


def player_pick_confirmation(request, pk, team_id):
    profile = request.user.profile
    player = Player.objects.get(sofifa_id=pk)
    team = Team.objects.get(id=team_id)
    group_players = team.belongs_group.group_players.all()
    if request.method == "POST":
        add_player_to_team_and_group(team, player)
        next_person = change_picking_person(team, profile)
        next_team = team.belongs_group.teams.get(owner=next_person)
        team.belongs_group.picking_person.add(next_person)
        pending_player_pick(next_person, next_team, team)
        messages.success(request, "Player picked!")
        return redirect("team", team.id)
    context = {
        "team": team,
        "profile": profile,
        "group_players": group_players,
        "player": player,
    }
    pick_alert(request, context)
    return render(request, "player-pick-confirmation.html", context)


def pending_player_pick_confirmation(request, pk, team_id):
    profile = request.user.profile
    player = Player.objects.get(sofifa_id=pk)
    team = Team.objects.get(id=team_id)
    group_players = team.belongs_group.group_players.all()
    if request.method == "POST":
        team.pending_player.add(player)
        team.save()
        messages.success(request, "Pending player added!")
        return redirect("team", team.id)
    context = {
        "team": team,
        "profile": profile,
        "group_players": group_players,
        "player": player,
    }
    pick_alert(request, context)
    return render(request, "pending-player-pick-confirmation.html", context)
