from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

# Create your models here.
class UserProfileManager(BaseUserManager):
    """Manager for user profiles """
    # manipulating the objects within the manager is formed
    def create_user(self, email, name, password=None):
        """ Create a new user Profile"""
        if not email:
            raise ValueError('User must have an email address')

        # Normalizing the eamil address(it simply lower case the second half of the email address)
        email = self.normalize_email(email)
        # creating a new model
        user = self.model(email=email, name=name)

        # it make sure the password is hashed
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with a given details """
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()
    # When django creates a user, by default it aspect to have a username and password CharField
    # But we have replaced the username field with email fied
    # So we just have to create a custom manager that can handle creating a user with email field instead of username field

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of the user"""
        return self.name
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name
    def __str__(self):
        """Return String representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
