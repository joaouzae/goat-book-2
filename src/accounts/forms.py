from django.contrib.auth.forms import UserCreationForm

from accounts.models import ListUser


class ListUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ListUser
        fields = ("email",)
