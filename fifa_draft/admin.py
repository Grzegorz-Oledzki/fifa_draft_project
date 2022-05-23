from django.contrib import admin
from fifa_draft.models import Profile, Group, Team, Player
from import_export.admin import ImportExportModelAdmin


admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(Team)


@admin.register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    list_display = ('sofifa_id', 'short_name', 'overall')