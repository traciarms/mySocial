from django.contrib import admin
from profile.models import Profile

__author__ = 'traciarms'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dob', 'gender']


admin.site.register(Profile, ProfileAdmin)
