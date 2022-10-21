from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from tablib import Dataset

from api.utils import group_available_players
from fifa_draft.models import Team
from players.models import Player
from players.utils import (add_player_to_team_and_group, change_picking_person,
                           last_and_first_picking_persons, pending_player_pick)


def upload_players(request: WSGIRequest) -> HttpResponse:
    if request.method == "POST":
        dataset = Dataset()
        new_player = request.FILES["myfile"]

        if not new_player.name.endswith("xlsx"):
            messages.error(request, "Wrong format")
            return render(request, "upload.html")

        imported_data = dataset.load(new_player.read(), format="xlsx")
        for data in imported_data:
            value = Player(*data)
            value.save()
            return render(request, "upload.html")


def players(request: WSGIRequest) -> HttpResponse:
    players = Player.objects.all()
    context = {"players": players}
    if request.user.is_authenticated:
        profile = request.user.profile
        context["profile"] = profile
    return render(request, "players.html", context)


@login_required(login_url="login")
def choose_team(request: WSGIRequest) -> HttpResponse:
    profile = request.user.profile
    teams = profile.draft_teams.all()
    context = {"teams": teams, "profile": profile}
    return render(request, "choose-team.html", context)


def players_pick(request: WSGIRequest, pk: str) -> HttpResponse:
    profile = request.user.profile
    team = Team.objects.get(id=pk)
    group = team.belongs_group
    players = group_available_players(group.id)
    picking_person = group.picking_person.all()
    context = {
        "team": team,
        "profile": profile,
        "players": players,
        "picking_person": picking_person,
    }
    if team.team_players.count() > 0:
        team_players = team.team_players.all()
        context["team_players"] = team_players
    if team.belongs_group.draft_order and profile not in group.picking_person.all():
        first_person, last_person = last_and_first_picking_persons(team)
        if team.pending_player.count() == 0 or profile == first_person and team.pending_player.count() == 1 and team.belongs_group.draft_order_choice == "Serpentine" or profile == last_person and team.pending_player.count() == 1 and team.belongs_group.draft_order_choice == "Serpentine":
            context["add_pending_player"] = True
    return render(request, "players-pick.html", context)


def player_pick_confirmation(
    request: WSGIRequest, pk: str, team_id: str
) -> HttpResponse:
    profile = request.user.profile
    player = Player.objects.get(sofifa_id=pk)
    team = Team.objects.get(id=team_id)
    group_players = team.belongs_group.group_players.all()
    if request.method == "POST" and team.owner == profile:
        add_player_to_team_and_group(team, player)
        next_person = change_picking_person(team, profile)
        next_team = team.belongs_group.teams.get(owner=next_person)
        team.belongs_group.picking_person.add(next_person)
        pending_player_pick(next_team, team)
        messages.success(request, "Player picked!")
        return redirect("team", team.id)
    context = {
        "team": team,
        "profile": profile,
        "group_players": group_players,
        "player": player,
    }
    return render(request, "player-pick-confirmation.html", context)


def pending_player_pick_confirmation(
    request: WSGIRequest, pk: str, team_id: str
) -> HttpResponse:
    profile = request.user.profile
    player = Player.objects.get(sofifa_id=pk)
    team = Team.objects.get(id=team_id)
    group_players = team.belongs_group.group_players.all()
    if request.method == "POST" and team.owner == profile:
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
    return render(request, "pending-player-pick-confirmation.html", context)


def delete_pending_player_pick_confirmation(
    request: WSGIRequest, pk: str, team_id: str
) -> HttpResponse:
    profile = request.user.profile
    player = Player.objects.get(sofifa_id=pk)
    team = Team.objects.get(id=team_id)
    if request.method == "POST" and team.owner == profile:
        team.pending_player.remove(player)
        team.save()
        messages.success(request, "Pending player deleted!")
        return redirect("team", team.id)
    context = {
        "team": team,
        "profile": profile,
        "player": player,
    }
    return render(request, "delete-pending-player-pick-confirmation.html", context)
