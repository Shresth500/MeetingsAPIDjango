from django.contrib import admin
from MeetingsAppApi import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Meetings)
admin.site.register(models.Attendee)