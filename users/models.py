from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Profile(models.Model):
    def validate_image(self):
        file_size = self.file.size
        limit_mb = 0.3 * 1024 * 1024
        if file_size > limit_mb:
            raise ValidationError(_("Featured image is too big (max 3mb)"))

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=False, null=False)
    short_intro = models.CharField(max_length=250, blank=True, null=True)
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="profile_images/", validators=[validate_image]
    )
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    draft_teams = models.ManyToManyField(
        "fifa_draft.Team", blank=True, related_name="draft_teams"
    )
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
            url = "http://dobrarobota.org/wp-content/uploads/2017/02/default-thumbnail.jpg"
        return url

    class Meta:
        ordering = ["created"]
