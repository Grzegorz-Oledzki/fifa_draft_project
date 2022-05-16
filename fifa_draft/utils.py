from fifa_draft.forms import GroupForm, TeamForm
from django.contrib import messages


def team_form_validation(request, form, profile):
    # if request.method == "POST":
    # form = TeamForm(request.POST, request.FILES)
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
        elif profile in team.belongs_group.members.all():
            messages.error(request, 'You have already team in this group')
        elif team.belongs_group.password != team.group_password:
            messages.error(request, 'Password error')
        elif not unique_name:
            messages.error(request, 'Please choose unique name')
    return form
