from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from players.models import Player


@admin.register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    list_display = ("sofifa_id", "short_name", "overall")
