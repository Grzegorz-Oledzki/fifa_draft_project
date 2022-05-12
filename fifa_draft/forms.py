from django.forms import ModelForm
from fifa_draft.models import Group, Profile, Team

class GroupForm(ModelForm):
    class Meta:
        model = Group
        owner = Profile
        fields = ['name', 'description', 'number_of_players', 'password', 'featured_image', 'draft_order_choice']
        labels = {"password": "Enter password, only letters"}

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input", "placeholder": "Add " + name})


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['belongs_group', 'name', 'featured_image', 'group_password', 'formation', 'description']
        labels = {"group_password": "Enter password, only letters"}


    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input", "placeholder": "Add " + name})
