def add_to_picking_history(profile, player, group):
    draft_history = str(profile.name) + " picked " + str(player.short_name) + ":"
    group.picking_history += draft_history
    group.save()


def add_player_to_team_and_group(team, player):
    team.belongs_group.picking_person.clear()
    team.team_players.add(player)
    team.belongs_group.group_players.add(player)
    team.belongs_group.save()
    team.save()
    add_to_picking_history(team.owner, player, team.belongs_group)
    team.pending_player.clear()


def last_and_first_picking_persons(team):
    group_profiles_order = team.belongs_group.profiles_order_as_list()
    last_person = team.belongs_group.members.get(
        name=group_profiles_order[team.belongs_group.members.count() - 1]
    )
    first_person = team.belongs_group.members.get(name=group_profiles_order[0])
    return first_person, last_person


def sum_of_team_players_is_equal_average_sum_of_other_group_teams_players(team):
    if (
        team.team_players.count()
        == team.belongs_group.group_players.count() / team.belongs_group.members.count()
        and team.team_players.count() != 0
    ):
        return True


def sum_of_team_players_is_greater_average_sum_of_other_group_teams_players(team):
    last_person = last_and_first_picking_persons(team)[1]
    last_team = team.belongs_group.team_set.get(owner=last_person)
    if (
        last_team.team_players.count()
        > team.belongs_group.group_players.count() / team.belongs_group.members.count()
    ):
        return True


def change_picking_person_for_serpentine_draft(
    team, next_profile_index, group_profiles_order, profile
):
    if sum_of_team_players_is_equal_average_sum_of_other_group_teams_players(team):
        return profile
    elif sum_of_team_players_is_greater_average_sum_of_other_group_teams_players(team):
        return team.belongs_group.members.get(
            name=group_profiles_order[next_profile_index - 2]
        )
    else:
        return team.belongs_group.members.get(
            name=group_profiles_order[next_profile_index]
        )


def change_picking_person_for_fixed_draft(
    team, next_profile_index, group_profiles_order
):
    if team.belongs_group.members.count() == next_profile_index:
        return team.belongs_group.members.get(name=group_profiles_order[0])
    else:
        return team.belongs_group.members.get(
            name=group_profiles_order[next_profile_index]
        )


def change_picking_person(team, profile):
    group_profiles_order = team.belongs_group.profiles_order_as_list()
    next_profile_index = group_profiles_order.index(str(profile.name)) + 1
    if team.belongs_group.draft_order_choice == "Serpentine":
        return change_picking_person_for_serpentine_draft(
            team, next_profile_index, group_profiles_order, profile
        )
    else:
        return change_picking_person_for_fixed_draft(
            team, next_profile_index, group_profiles_order
        )


def pending_player_next_person_add(team):
    team.belongs_group.picking_person.clear()
    next_person = change_picking_person(team, team.owner)
    team.belongs_group.picking_person.add(next_person)


def is_pending_player_and_pending_player_not_in_group_players(next_team, team):
    return (
        next_team.pending_player.count() > 0
        and next_team.pending_player.all() not in team.belongs_group.group_players.all()
    )


def is_pending_team_owner_is_picking_person_and_have_pending_player(pending_team, team):
    return (
        pending_team.owner in team.belongs_group.picking_person.all()
        and pending_team.pending_player.count() > 0
    )


def check_count_of_pending_players_and_add_to_team_and_change_picking_person(
    pending_team, team
):

    if pending_team.pending_player.all().count() == 2:
        for player in pending_team.pending_player.all():
            if player not in team.belongs_group.group_players.all():
                add_player_to_team_and_group(pending_team, player)
                pending_player_next_person_add(pending_team)
    elif (
        pending_team.pending_player.get() not in team.belongs_group.group_players.all()
    ):
        add_player_to_team_and_group(pending_team, pending_team.pending_player.get())
        pending_player_next_person_add(pending_team)


def pending_player_pick(next_team, team):
    if is_pending_player_and_pending_player_not_in_group_players:
        for _ in team.belongs_group.members.all():
            for pending_team in team.belongs_group.team_set.all():
                if is_pending_team_owner_is_picking_person_and_have_pending_player(
                    pending_team, team
                ):
                    check_count_of_pending_players_and_add_to_team_and_change_picking_person(
                        pending_team, team
                    )
    else:
        pending_player_next_person_add(next_team)
