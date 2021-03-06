from fifa_draft.models import Group


def pick_alert(request):
    context = {}
    if request.user.is_authenticated:
        group_ids = []
        profile = request.user.profile
        groups = Group.objects.all()
        for group in groups:
            if profile in group.picking_person.all():
                group_ids.append(group.id)
                context["pick_alert"] = True
                context["group_ids"] = group_ids
                return context
            else:
                return context
    else:
        return context
