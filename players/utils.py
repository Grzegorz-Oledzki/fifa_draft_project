

def change_picking_person(team, profile):
    group_profiles_order = team.belongs_group.profiles_order_as_list()[:-1]
    next_profile_index = group_profiles_order.index(str(profile.username)) + 1
    last_person = team.belongs_group.members.get(
        username=group_profiles_order[team.belongs_group.members.count() - 1]
    )
    last_team = team.belongs_group.team_set.get(owner=last_person)
    if team.belongs_group.draft_order_choice == "Serpentine":
        if (
            team.team_players.count()
            == team.belongs_group.group_players.count()
            / team.belongs_group.members.count()
            and team.team_players.count() != 0
        ):
            team.belongs_group.picking_person.add(profile)
        elif (
            last_team.team_players.count()
            > team.belongs_group.group_players.count()
            / team.belongs_group.members.count()
        ):
            team.belongs_group.picking_person.add(
                team.belongs_group.members.get(
                    username=group_profiles_order[next_profile_index - 2]
                )
            )
        else:
            team.belongs_group.picking_person.add(
                team.belongs_group.members.get(
                    username=group_profiles_order[next_profile_index]
                )
            )
    else:
        if team.belongs_group.members.count() == next_profile_index:
            team.belongs_group.picking_person.add(
                team.belongs_group.members.get(username=group_profiles_order[0])
            )
        else:
            team.belongs_group.picking_person.add(
                team.belongs_group.members.get(
                    username=group_profiles_order[next_profile_index]
                )
            )
