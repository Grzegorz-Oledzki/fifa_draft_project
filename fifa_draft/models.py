from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from users.models import Profile
from players.models import Player


class Group(models.Model):
    class DraftOrders(models.TextChoices):
        SERPENTINE = (_("Serpentine"),)
        FIXED = _("Fixed")

    owner = models.ForeignKey(
        'users.Profile',
        default='users.Profile',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    members = models.ManyToManyField(
        'users.Profile', blank=True, default='users.Profile', related_name="members"
    )
    teams = models.ManyToManyField("Team", blank=True, related_name="teams")
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to="group_images/")
    password = models.CharField(null=False, blank=False, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    number_of_players = models.PositiveIntegerField(
        validators=[MinValueValidator(14), MaxValueValidator(20)]
    )
    draft_order_choice = models.CharField(
        blank=False,
        choices=DraftOrders.choices,
        max_length=10,
        default=DraftOrders.SERPENTINE,
    )
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    group_players = models.ManyToManyField(
        Player, blank=True, related_name="group_players"
    )
    picking_person = models.ManyToManyField(
        'users.Profile', blank=True, default='users.Profile', related_name="picking_person"
    )
    draft_order = models.CharField(max_length=200, blank=True, null=True)

    def draft_order_as_list(self):
        return self.draft_order.split("\n")

    def profiles_order_as_list(self):
        persons = self.draft_order.split("\n")
        profiles_order = []
        for person in persons:
            profiles_order.append(person[3::])
        return profiles_order

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["created"]

    def image_url(self):
        try:
            url = self.featured_image.url
        except:
            url = "http://dobrarobota.org/wp-content/uploads/2017/02/default-thumbnail.jpg"
        return url


class Team(models.Model):
    FORMATION_CHOICES = (
        ("4–4–2", "4–4–2"),
        ("4–3–3", "4–3–3"),
        ("4–1–2-1-2", "4–1–2-1-2"),
        ("4–4–1–1", "4–4–1–1"),
        ("4–3–2–1", "4–3–2–1"),
        ("4-2-3-1", "4-2-3-1"),
        ("3–4–3", "3–4–3"),
        ("5–3–2", "5–3–2"),
    )
    owner = models.ForeignKey(
        'users.Profile', default='users.Profile', null=False, blank=False, on_delete=models.CASCADE
    )
    belongs_group = models.ForeignKey(
        Group, null=False, blank=False, on_delete=models.CASCADE, db_constraint=False
    )
    name = models.CharField(max_length=20, blank=False, null=False)
    featured_image = models.ImageField(null=True, blank=True, upload_to="team_images/")
    created = models.DateTimeField(auto_now_add=True)
    group_password = models.CharField(null=False, blank=False, max_length=50)
    max_players = models.PositiveIntegerField(default=14, blank=False)
    formation = models.CharField(
        blank=False,
        choices=FORMATION_CHOICES,
        max_length=10,
        default=FORMATION_CHOICES[1],
    )
    description = models.TextField(null=True, blank=True)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    team_players = models.ManyToManyField(
        Player, blank=True, related_name="team_players"
    )
    pending_player = models.ManyToManyField(
        Player, blank=True, related_name="pending_player"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["created"]

    def image_url(self):
        try:
            url = self.featured_image.url
        except:
            url = "http://dobrarobota.org/wp-content/uploads/2017/02/default-thumbnail.jpg"
        return url



