from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator


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
        default="profile_images/user-default.png",
    )
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
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
    owner = models.ForeignKey(Profile, default=Profile, null=False, blank=False, on_delete=models.CASCADE)
    members = models.ManyToManyField(Profile, blank=True, related_name='members')
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    password = models.CharField(null=False, blank=False, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    number_of_players = models.PositiveIntegerField(default=18, validators=[MinValueValidator(14), MaxValueValidator(20)])
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["created"]

    def clean(self):
        if self.number_of_players < 14 or self.number_of_players > 20:
            raise ValidationError(_('Only number of player 14 to 20 accepted.'))

