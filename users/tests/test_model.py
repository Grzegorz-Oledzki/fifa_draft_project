from users.models import Profile
from django.contrib.auth.models import User

profile_data = {
    "username": "grzes te11",
    "password": "abc"
}


def test_create_profile() -> None:
    user = User.objects.create(**profile_data)
    profile = Profile.objects.get(id=user.profile.id)
    assert type(profile) == Profile
    profile.delete()
