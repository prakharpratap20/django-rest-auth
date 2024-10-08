from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    """
    A model to represent a user profile in the system.
    This model extends the User model from Django.
    """
    user = (
        models.OneToOneField(User, on_delete=models.CASCADE,
                             related_name="profile"),
    )
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"
