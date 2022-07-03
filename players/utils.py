

def add_player_to_team_and_group(team, player):
    team.belongs_group.picking_person.clear()
    team.team_players.add(player)
    team.belongs_group.group_players.add(player)
    team.belongs_group.save()
    team.save()
    team.pending_player.clear()


def last_and_first_picking_persons(team):
    group_profiles_order = team.belongs_group.profiles_order_as_list()[:-1]
    last_person = team.belongs_group.members.get(
        name=group_profiles_order[team.belongs_group.members.count() - 1])
    first_person = team.belongs_group.members.get(
        name=group_profiles_order[team.belongs_group.members.count() - team.belongs_group.members.count()])
    return first_person, last_person


def change_picking_person(team, profile):
    group_profiles_order = team.belongs_group.profiles_order_as_list()[:-1]
    next_profile_index = group_profiles_order.index(str(profile.name)) + 1
    last_person = last_and_first_picking_persons(team)[1]
    last_team = team.belongs_group.team_set.get(owner=last_person)
    if team.belongs_group.draft_order_choice == "Serpentine":
        if (
            team.team_players.count()
            == team.belongs_group.group_players.count()
            / team.belongs_group.members.count()
            and team.team_players.count() != 0
        ):
            return profile
        elif (
            last_team.team_players.count()
            > team.belongs_group.group_players.count()
            / team.belongs_group.members.count()
        ):
            return team.belongs_group.members.get(
                    name=group_profiles_order[next_profile_index - 2]
                )
        else:
            return team.belongs_group.members.get(
                    name=group_profiles_order[next_profile_index]
                )
    else:
        if team.belongs_group.members.count() == next_profile_index:
            return team.belongs_group.members.get(name=group_profiles_order[0])
        else:
            return team.belongs_group.members.get(
                    name=group_profiles_order[next_profile_index]
                )


def pending_player_next_person_add(team):
    team.belongs_group.picking_person.clear()
    next_person = change_picking_person(team, team.owner)
    team.belongs_group.picking_person.add(next_person)


def pending_player_pick(next_person, next_team, team):
    if next_team.pending_player.count() > 0 and next_team.pending_player.all() not in team.belongs_group.group_players.all():
        for pending_team in team.belongs_group.team_set.all():
            if pending_team.owner in team.belongs_group.picking_person.all() and pending_team.pending_player.count() > 0:
                if pending_team.pending_player.all().count() == 2:
                    for player in pending_team.pending_player.all():
                        if player not in team.belongs_group.group_players.all():
                            add_player_to_team_and_group(pending_team, player)
                            pending_player_next_person_add(team)
                elif pending_team.pending_player.get() not in team.belongs_group.group_players.all():
                    add_player_to_team_and_group(pending_team, pending_team.pending_player.get())
                    pending_player_next_person_add(team)
    else:
        team.belongs_group.picking_person.add(next_person)
