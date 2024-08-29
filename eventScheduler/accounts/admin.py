from django.contrib import admin
from .models import UserProfile

# Register your models here.


# Register the UserProfile model with the admin site.
admin.site.register(UserProfile)

# Change the admin site header to "events scheduler".
admin.site.site_header = "events scheduler"
