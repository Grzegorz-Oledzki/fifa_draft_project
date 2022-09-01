import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from players.models import Player
from users.models import Profile


class Group(models.Model):
    class DraftOrders(models.TextChoices):
        SERPENTINE = (_("Serpentine"),)
        FIXED = _("Fixed")

    def validate_image(self):
        file_size = self.file.size
        limit_mb = 3 * 1024 * 1024
        if file_size > limit_mb:
            raise ValidationError("Featured image is too big (max 3mb)")

    owner = models.ForeignKey(
        "users.Profile",
        default="users.Profile",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    members = models.ManyToManyField(
        "users.Profile", blank=True, default="users.Profile", related_name="members"
    )
    teams = models.ManyToManyField("Team", blank=True, related_name="teams")
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, upload_to="group_images/", validators=[validate_image], default="default-thumbnail.jpg"
    )
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
        "users.Profile",
        blank=True,
        default="users.Profile",
        related_name="picking_person",
    )
    draft_order = models.CharField(max_length=200, blank=True, null=True)
    picking_history = models.CharField(max_length=10000000, blank=True, null=True)

    def picking_history_as_list(self) -> List[str]:
        return self.picking_history.split(":")

    def profiles_order_as_list(self) -> List[str]:
        persons = self.draft_order.split(":")
        profiles_order = [person for person in persons]
        profiles_order.pop(-1)
        return profiles_order

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["created"]

    def image_url(self) -> Union[ImageFieldFile, str]:
        try:
            url = self.featured_image.url
        except:
            url = "https://grzes-bucket2.s3.eu-central-1.amazonaws.com/default-thumbnail.jpg"
        return url


class Team(models.Model):
    def validate_image(self):
        file_size = self.file.size
        limit_mb = 3 * 1024 * 1024
        if file_size > limit_mb:
            raise ValidationError(_("Featured image is too big (max 3mb)"))

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
        "users.Profile",
        default="users.Profile",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    belongs_group = models.ForeignKey(
        Group, null=False, blank=False, on_delete=models.CASCADE, db_constraint=False
    )
    name = models.CharField(max_length=20, blank=False, null=False)
    featured_image = models.ImageField(
        null=True, blank=True, upload_to="team_images/", validators=[validate_image]
    )
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

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["created"]

    def image_url(self) -> Union[ImageFieldFile, str]:
        try:
            url = self.featured_image.url
        except:
            url = "https://grzes-bucket2.s3.eu-central-1.amazonaws.com/default-thumbnail.jpg"
        return url
