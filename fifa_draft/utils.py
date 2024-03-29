from typing import Callable, List, Any

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest

from fifa_draft.forms import EditTeamForm, TeamForm
from fifa_draft.models import Group, Team
from users.models import Profile


def is_team_name_unique_in_group(team_name: str, group: Group, profile) -> bool:
    for team_in_group in group.teams.all():
        if (
            str(team_in_group).lower() == team_name.lower()
            and profile != team_in_group.owner
        ):
            return False
    return True


def get_group_players_by_history(group: Group) -> list:
    picked_players_oder_by_history = [group.group_players.get(sofifa_id=pick) for pick in group.picking_history_as_list()]
    return picked_players_oder_by_history


def create_team(team: Team, profile: Profile) -> None:
    team.owner = profile
    team.max_players = team.belongs_group.number_of_players
    team.save()
    team.belongs_group.members.add(profile)
    profile.draft_teams.add(team)
    team.belongs_group.teams.add(team)


def team_form_validation(
    request: WSGIRequest, form: TeamForm, profile: Profile
) -> bool:
    is_form_valid = False
    if form.is_valid():
        team = form.save(commit=False)
        unique_name = is_team_name_unique_in_group(str(team.name), team.belongs_group, profile)
        if (
            team.belongs_group.password == team.group_password
            and profile not in team.belongs_group.members.all()
            and unique_name
        ):
            create_team(team, profile)
            messages.success(request, "Team created and added to group successful!")
            is_form_valid = True
            return is_form_valid
        elif team.belongs_group.password != team.group_password:
            messages.error(request, "Password error")
        elif not unique_name:
            messages.error(request, "Please choose unique name")
        elif profile in team.belongs_group.members.all():
            messages.error(request, "You have already team in this group")
        return is_form_valid
    else:
        messages.error(request, "Featured image is too big (max 3mb)")
    return is_form_valid


def edit_team_form_validation(request: WSGIRequest, form: EditTeamForm) -> bool:
    form_valid = False
    profile = request.user.profile
    if form.is_valid():
        team = form.save(commit=False)
        unique_name = is_team_name_unique_in_group(str(team.name), team.belongs_group, profile)
        if team.belongs_group.password == team.group_password and unique_name:
            team.save()
            form_valid = True
            messages.success(request, "Team edited successful!")
            return form_valid
        elif not unique_name:
            messages.error(request, "Please choose unique name")
        elif team.belongs_group.password != team.group_password:
            messages.error(request, "Password error")
    else:
        messages.error(request, "Featured image is too big (max 3mb)")
    return form_valid


def draw_draft_order(group: Group) -> None:
    profiles_order = []
    draw_order = ""
    for member in group.members.all().order_by("?"):
        draw_order += str(member.name) + ":"
        profiles_order.append(member)
    group.picking_person.add(profiles_order[0])
    group.draft_order = draw_order
    group.picking_history = ""


def group_validation(request: WSGIRequest, group: Group) -> None:
    if group.featured_image.size > 3 * 1024 * 1024:
        messages.error(request, "Featured image is too big (max 3mb)")
    elif group.number_of_players > 20 or group.number_of_players < 14:
        messages.error(request, "Number of players must be between 14 and 20")
    else:
        messages.error(request, "Group name is not unique")
