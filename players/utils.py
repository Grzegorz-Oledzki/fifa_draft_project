

def add_player_to_team_and_group(team, player):
    team.belongs_group.picking_person.clear()
    team.team_players.add(player)
    team.belongs_group.group_players.add(player)
    team.belongs_group.save()
    team.save()
    team.pending_player.clear()


def change_picking_person(team, profile, added_value):
    group_profiles_order = team.belongs_group.profiles_order_as_list()[:-1]
    next_profile_index = group_profiles_order.index(str(profile.name)) + 1 + added_value
    last_person = team.belongs_group.members.get(
        name=group_profiles_order[team.belongs_group.members.count() - 1]
    )
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


def picking_pending_player(team, next_team, next_person):
    while next_team.pending_player.count() > 0:
        add_player_to_team_and_group(next_team, next_team.pending_player.get())
        team.belongs_group.picking_person.add(next_person)
