from django.db import models
from django.utils.translation import gettext_lazy as _


class Player(models.Model):
    sofifa_id = models.IntegerField(_("sofifa_id"), default=False)
    player_url = models.CharField(_("player_url"), max_length=150, default=False)
    short_name = models.CharField(_("short_name"), max_length=50, default=False)
    player_positions = models.CharField(
        _("player_positions"), max_length=15, null=True, default=False
    )
    overall = models.IntegerField(_("overall"), null=True)
    age = models.IntegerField(_("age"), null=True)
    height_cm = models.IntegerField(_("height_cm"), null=True)
    weight_kg = models.IntegerField(_("weight_kg"), null=True)
    club_name = models.CharField(
        _("club_name"), max_length=50, null=True, default=False
    )
    preferred_foot = models.CharField(
        _("preferred_foot"), max_length=6, null=True, default=False
    )
    weak_foot = models.IntegerField(_("weak_foot"), null=True)
    skill_moves = models.IntegerField(_("skill_moves"), null=True)
    work_rate = models.CharField(
        _("work_rate"), max_length=50, null=True, default=False
    )
    pace = models.IntegerField(_("pace"), null=True)
    shooting = models.IntegerField(_("shooting"), null=True)
    passing = models.IntegerField(_("passing"), null=True)
    dribbling = models.IntegerField(_("dribbling"), null=True)
    defending = models.IntegerField(_("defending"), null=True)
    physic = models.IntegerField(_("physic"), null=True)
    player_face_url = models.CharField(
        _("player_face_url"), max_length=200, null=True, default=False
    )
    club_logo_url = models.CharField(
        _("club_logo_url"), max_length=200, null=True, default=False
    )
    nation_flag_url = models.CharField(
        _("nation_flag_url"), max_length=200, null=True, default=False
    )

    def __str__(self) -> str:
        return self.short_name

    class Meta:
        ordering = ["-overall"]
