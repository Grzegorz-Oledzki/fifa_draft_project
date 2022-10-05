from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from fifa_draft.models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {"first_name": "Name"}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input", "placeholder": "Add " + name})

        self.fields["first_name"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Enter your name/nickname",
            }
        )
        self.fields["username"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Remember your username, as it will be used to log in",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Enter a password that meets the following requirements",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Confirm password",
            }
        )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "username",
            "email",
            "location",
            "short_intro",
            "profile_image",
            "social_github",
            "social_twitter",
            "social_linkedin",
            "social_youtube",
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields["profile_image"].label = "Profile image (max 3mb)"

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input", "placeholder": "Add " + name})
