from django.contrib import admin
from players.models import Player
from import_export.admin import ImportExportModelAdmin


@admin.register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    list_display = ("sofifa_id", "short_name", "overall")
