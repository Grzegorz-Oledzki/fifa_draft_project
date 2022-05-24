from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    short_intro = models.CharField(max_length=250, blank=True, null=True)
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile_images/",
    )
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    draft_teams = models.ManyToManyField("Team", blank=True, related_name="draft_teams")
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.username)

    @property
    def image_url(self):
        try:
            url = self.profile_image.url
        except:
            url = "https://grzesczes-bucket.s3.amazonaws.com/profile_images/user-default.png"
        return url

    class Meta:
        ordering = ["created"]


class Group(models.Model):
    class DraftOrders(models.TextChoices):
        SERPENTINE = (_("Serpentine"),)
        FIXED = _("Fixed")

    owner = models.ForeignKey(
        Profile,
        default=Profile,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    members = models.ManyToManyField(
        Profile, blank=True, default=Profile, related_name="members"
    )
    teams = models.ManyToManyField("Team", blank=True, related_name="teams")
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to="group_images/")
    password = models.CharField(null=False, blank=False, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    number_of_players = models.PositiveIntegerField(
        default=18, validators=[MinValueValidator(14), MaxValueValidator(20)]
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
    group_players = models.ManyToManyField("Player", blank=True, related_name="group_players")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["created"]

    def image_url(self):
        try:
            url = self.featured_image.url
        except:
            url = "https://grzesczes-bucket.s3.amazonaws.com/default.jpg"
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
        ("5–3–2", "5–3–2")
    )
    owner = models.ForeignKey(
        Profile, default=Profile, null=False, blank=False, on_delete=models.CASCADE
    )
    belongs_group = models.ForeignKey(
        Group, null=False, blank=False, on_delete=models.CASCADE, db_constraint=False
    )
    name = models.CharField(max_length=200, blank=False, null=False)
    featured_image = models.ImageField(null=True, blank=True, upload_to="team_images/")
    created = models.DateTimeField(auto_now_add=True)
    group_password = models.CharField(null=False, blank=False, max_length=50)
    max_players = models.PositiveIntegerField(default=14, blank=False)
    formation = models.CharField(blank=False, choices=FORMATION_CHOICES, max_length=10, default=FORMATION_CHOICES[1])
    description = models.TextField(null=True, blank=True)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    team_players = models.ManyToManyField("Player", blank=True, related_name="team_players")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["created"]

    def image_url(self):
        try:
            url = self.featured_image.url
        except:
            url = "https://grzesczes-bucket.s3.amazonaws.com/default.jpg"
        return url


class Player(models.Model):
    sofifa_id = models.IntegerField(_('sofifa_id'), default=False)
    player_url = models.CharField(_("player_url"), max_length=150, default=False)
    short_name = models.CharField(_("short_name"), max_length=50, default=False)
    player_positions = models.CharField(_("player_positions"), max_length=15, null=True, default=False)
    overall = models.IntegerField(_("overall"), null=True)
    age = models.IntegerField(_("age"), null=True)
    height_cm = models.IntegerField(_("height_cm"), null=True)
    weight_kg = models.IntegerField(_("weight_kg"), null=True)
    club_name = models.CharField(_("club_name"), max_length=50, null=True, default=False)
    preferred_foot = models.CharField(_("preferred_foot"), max_length=6, null=True, default=False)
    weak_foot = models.IntegerField(_("weak_foot"), null=True)
    skill_moves = models.IntegerField(_("skill_moves"), null=True)
    work_rate = models.CharField(_("work_rate"), max_length=50, null=True, default=False)
    pace = models.IntegerField(_("pace"), null=True)
    shooting = models.IntegerField(_("shooting"), null=True)
    passing = models.IntegerField(_("passing"), null=True)
    dribbling = models.IntegerField(_("dribbling"), null=True)
    defending = models.IntegerField(_("defending"), null=True)
    physic = models.IntegerField(_("physic"), null=True)
    player_face_url = models.CharField(_("player_face_url"), max_length=200, null=True, default=False)
    club_logo_url = models.CharField(_("club_logo_url"), max_length=200, null=True, default=False)
    nation_flag_url = models.CharField(_("nation_flag_url"), max_length=200, null=True, default=False)

    def __str__(self):
        return self.short_name









