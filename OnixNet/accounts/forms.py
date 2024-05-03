from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if not Group.objects.filter(name="Users").exists():
                group = Group.objects.create(name="Users")
            else:
                group = Group.objects.get(name="Users")
            user.groups.add(group)
        return user
