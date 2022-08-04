from django.shortcuts import render, redirect
from fifa_draft.forms import (
    GroupForm,
    TeamForm,
    EditTeamForm,
    EditGroupForm,
    ChoosePersonPickingForm,
)
from fifa_draft.models import Group, Team
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from fifa_draft.utils import (
    team_form_validation,
    edit_team_form_validation,
    draw_draft_order,
    group_validation
)


def home(request):
    return render(request, "home.html")


def groups(request):
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, "groups.html", context)


def group(request, pk):
    group = Group.objects.get(id=pk)
    context = {"group": group}
    if request.user.is_authenticated:
        profile = request.user.profile
        context["profile"] = profile
    return render(request, "group.html", context)


@login_required(login_url="login")
def create_group(request):
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
            group_validation(request, group)
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


def team(request, pk):
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


def draft_order(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == "POST":
        draw_draft_order(group)
        group.save()
        messages.success(request, "Draw completed, see results under Excel sheet")
        return redirect("group", group.id)
    context = {"group": group}
    return render(request, "draft-order.html", context)


def choose_person_to_pick_players(request, pk):
    group = Group.objects.get(id=pk)
    form = ChoosePersonPickingForm(instance=group)
    if request.method == "POST":
        form = ChoosePersonPickingForm(request.POST, instance=group)
        form.save()
        return redirect("group", group.id)
    context = {"form": form}
    return render(request, "choose-picking-person.html", context)
