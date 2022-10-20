from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render

from fifa_draft.forms import (ChoosePersonPickingForm, EditGroupForm,
                              EditTeamForm, GroupForm, TeamForm)
from fifa_draft.models import Group, Team
from fifa_draft.utils import (draw_draft_order, edit_team_form_validation,
                              group_validation, team_form_validation, get_group_players_by_history)


def home(request: WSGIRequest) -> HttpResponse:
    return render(request, "home.html")


def all_groups(request: WSGIRequest) -> HttpResponse:
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, "groups.html", context)


def single_group(request: WSGIRequest, pk: str) -> HttpResponse:
    group = Group.objects.get(id=pk)
    players = get_group_players_by_history(group)
    context = {"group": group, "players": players}
    if request.user.is_authenticated:
        profile = request.user.profile
        context["profile"] = profile
    return render(request, "group.html", context)


@login_required(login_url="login")
def create_group(request: WSGIRequest) -> HttpResponse:
    form = GroupForm()
    profile = request.user.profile
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        group = form.save(commit=False)
        if form.is_valid():
            group.owner = profile
            group.picking_history = "Draft started " + "\n"
            form.save()
            messages.success(request, "Now create a team!")
            return redirect("create-team")
        else:
            group_validation(request, group)
    context = {"form": form}
    return render(request, "group-form.html", context)


@login_required(login_url="login")
def edit_group(request: WSGIRequest, pk: str) -> HttpResponse:
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
            group_validation(request, group)
    context = {"form": form, "group": group, "groups": groups}
    return render(request, "group-form.html", context)


def delete_group(request: WSGIRequest, pk: str) -> HttpResponse:
    group = Group.objects.get(id=pk)
    if request.method == "POST":
        group.delete()
        messages.success(request, "Group was deleted successful!")
        return redirect("home")
    context = {"group": group}
    return render(request, "delete-group.html", context)


def team(request: WSGIRequest, pk: str) -> HttpResponse:
    team = Team.objects.get(id=pk)
    players = team.team_players.all()
    pending_player = team.pending_player.all()
    context = {
        "team": team,
        "players": players,
        "pending_player": pending_player,
    }
    if request.user.is_authenticated:
        profile = request.user.profile
        context["profile"] = profile
    return render(request, "team.html", context)


@login_required(login_url="login")
def create_team(request: WSGIRequest) -> HttpResponse:
    form = TeamForm()
    profile = request.user.profile
    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        form_valid = team_form_validation(request, form, profile)
        if form_valid:
            team = form.save(commit=False)
            return redirect("group", team.belongs_group.id)
    context = {"form": form}
    return render(request, "team-form.html", context)


def edit_team(request: WSGIRequest, pk: str) -> HttpResponse:
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


def draft_order(request: WSGIRequest, pk: str) -> HttpResponse:
    group = Group.objects.get(id=pk)
    if request.method == "POST":
        draw_draft_order(group)
        group.save()
        messages.success(request, "Draw completed, see results under Excel sheet")
        return redirect("group", group.id)
    context = {"group": group}
    return render(request, "draft-order.html", context)


def choose_person_to_pick_players(request: WSGIRequest, pk: str) -> HttpResponse:
    group = Group.objects.get(id=pk)
    form = ChoosePersonPickingForm(instance=group)
    if request.method == "POST":
        form = ChoosePersonPickingForm(request.POST, instance=group)
        form.save()
        return redirect("group", group.id)
    context = {"form": form}
    return render(request, "choose-picking-person.html", context)


def draft_history(request: WSGIRequest, pk: str) -> HttpResponse:
    group = Group.objects.get(id=pk)
    draft_picking_history = group.picking_history_as_list()
    context = {"draft_picking_history": draft_picking_history}
    return render(request, "draft-history.html", context)
