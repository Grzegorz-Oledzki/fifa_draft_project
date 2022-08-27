import random

from django.contrib import messages


def is_unique_name(team):
    unique_name = True
    for team_in_group in team.belongs_group.teams.all():
        if (
            str(team_in_group).lower() == str(team).lower()
            and team.owner != team_in_group.owner
        ):
            unique_name = False
    return unique_name


def team_form_validation(request, form, profile):
    form_valid = False
    if form.is_valid():
        team = form.save(commit=False)
        unique_name = is_unique_name
        if (
            team.belongs_group.password == team.group_password
            and profile not in team.belongs_group.members.all()
            and unique_name
        ):
            team.owner = profile
            team.max_players = team.belongs_group.number_of_players
            team.save()
            team.belongs_group.members.add(profile)
            profile.draft_teams.add(team)
            team.belongs_group.teams.add(team)
            messages.success(request, "Team created and added to group successful!")
            form_valid = True
            return form_valid
        elif team.belongs_group.password != team.group_password:
            messages.error(request, "Password error")
        elif not unique_name:
            messages.error(request, "Please choose unique name")
        elif profile in team.belongs_group.members.all():
            messages.error(request, "You have already team in this group")
        return form_valid
    else:
        messages.error(request, "Featured image is too big (max 3mb)")


def edit_team_form_validation(request, form):
    form_valid = False
    if form.is_valid():
        team = form.save(commit=False)
        unique_name = is_unique_name(team)
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


def draw_draft_order(group):
    profiles_order = []
    draw_order = ""
    for member in group.members.all().order_by("?"):
        draw_order += str(member.name) + ":"
        profiles_order.append(member)
    group.picking_person.add(profiles_order[0])
    group.draft_order = draw_order
    group.picking_history = "Draft started!:"


def group_validation(request, group):
    if group.featured_image.size > 3 * 1024 * 1024:
        messages.error(request, "Featured image is too big (max 3mb)")
    elif group.number_of_players > 20 or group.number_of_players < 14:
        messages.error(request, "Number of players must be between 14 and 20")
    else:
        messages.error(request, "Group name is not unique")
