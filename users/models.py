from django.db import models
import uuid
from fifa_draft.models import Profile, Team
from django.utils.translation import gettext_lazy as _


class Formation(models.Model):
    class Formations(models.TextChoices):
        first = _('4–4–2'),
        second = _('4–3–3'),
        third = _('4–1–2-1-2'),
        fourth = _('4–4–1–1'),
        fifth = _('4–3–2–1'),
        sixth = _('4-2-3-1'),
        seventh = _('3–4–3'),
        eighth = _('5–3–2')

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    formation = models.CharField(max_length=10, blank=False, choices=Formations.choices, default=Formations.first)
    description = models.TextField(null=True, blank=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    def __str__(self):
        return self.formation