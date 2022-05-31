from django.forms import ModelForm
from fifa_draft.models import Group, Profile, Team, Player
from django.utils.translation import gettext_lazy as _
from django import forms


class GroupForm(ModelForm):
    class Meta:
        model = Group
        owner = Profile
        fields = [
            "name",
            "description",
            "number_of_players",
            "password",
            "featured_image",
            "draft_order_choice",
        ]

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.fields["password"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Enter a password so that other people can add the team to your group.",
            }
        )
        self.fields["name"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Name of group, eg. Fifa maniacs 10.05.2022",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Group description, eg. when and where you will be playing the tournament",
            }
        )
        self.fields["number_of_players"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "The number of players can range from 14 to 20.",
            }
        )


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = [
            "belongs_group",
            "name",
            "featured_image",
            "group_password",
            "formation",
            "description",
        ]
        labels = {"group_password": "Enter group password"}

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "input", "placeholder": "Add team " + name}
            )
        self.fields["group_password"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Your password must be the same as the group password",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Add team description, eg. wings wide, wings converge inward ",
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

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input", "placeholder": "Add " + name})


class EditGroupForm(ModelForm):
    class Meta:
        model = Group
        owner = Profile
        fields = [
            "name",
            "description",
            "number_of_players",
            "featured_image",
            "draft_order_choice",
        ]

    def __init__(self, *args, **kwargs):
        super(EditGroupForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input", "placeholder": "Add " + name})
        self.fields["name"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Name of group, eg. Fifa maniacs 10.05.2022",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Group description, eg. when and where you will be playing the tournament",
            }
        )
        self.fields["number_of_players"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "The number of players can range from 14 to 20.",
            }
        )


class EditTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = [
            "name",
            "featured_image",
            "formation",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super(EditTeamForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input", "placeholder": "Add " + name})
        self.fields["description"].widget.attrs.update(
            {
                "class": "input",
                "placeholder": "Add team description, eg. wings wide, wings converge inward ",
            }
        )


class ChoosePersonPickingForm(ModelForm):
    class Meta:
        model = Group
        fields = ["picking_person"]
        widgets = {"picking_person": forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super(ChoosePersonPickingForm, self).__init__(*args, **kwargs)
        self.picking_people_choices = Profile.objects.filter(members=self.instance)
        self.fields["picking_person"].queryset = self.picking_people_choices


class DraftOrderForm(ModelForm):
    class Meta:
        model = Group
        fields = ["draft_order"]
