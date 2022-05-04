from django.forms import ModelForm
from fifa_draft.models import Group, Profile

class GroupForm(ModelForm):
    class Meta:
        model = Group
        owner = Profile
        fields = ['name', 'description', 'number_of_players', 'password', 'featured_image', 'owner']

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input", "placeholder": "Add " + name})