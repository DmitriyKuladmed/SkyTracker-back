from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("У пользователя должен быть email")
        if not username:
            raise ValueError("У пользователя должен быть никнейм")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
