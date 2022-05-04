from django.forms import ModelForm
from fifa_draft.models import Group, Profile

class GroupForm(ModelForm):
    class Meta:
        model = Group
        owner = Profile
        fields = ['name', 'description', 'number_of_players', 'password', 'featured_image', 'owner']