from django.contrib import admin
from django.contrib.auth.models import User
from profile.models import Profile, Image, WallPost, PostComment

__author__ = 'traciarms'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dob', 'gender']


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image']


class WallPostAdmin(admin.ModelAdmin):
    list_display = ['author', 'posted_to', 'message', 'posted_at']


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'wall_post', 'comment', 'posted_at']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(WallPost, WallPostAdmin)
admin.site.register(PostComment, PostCommentAdmin)