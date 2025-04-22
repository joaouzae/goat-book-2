from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, email):
        return User.objects.create(email=email)

    def create_superuser(self, email, password):
        self.create_user(email)


class User(AbstractBaseUser):
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    is_anonymous = False
    is_authenticated = True

    objects: UserManager = UserManager()
