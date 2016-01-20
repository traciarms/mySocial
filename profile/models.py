from django.contrib.auth.models import User
from django.db import models
from myfacebook.settings import MEDIA_ROOT

__author__ = 'traciarms'


class Profile(models.Model):
    FEMALE = 'F'
    MALE = 'M'
    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male')
    )
    user = models.OneToOneField(User)
    dob = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                              verbose_name='Gender')
    phone = models.CharField(max_length=10)
    profile_thumbnail = models.ImageField(null=True)

    def __str__(self):
        return ("User: {}, DOB: {}, Gender: {}, Phone: {}".
                format(self.user, self.dob, self.gender, self.phone))


# class Image(models.Model):
#     image = models.ImageField(upload_to=MEDIA_ROOT)
#     profile = models.ManyToOneRel(Profile)


# class WallPost(models.Model):
#     author = models.ForeignKey(User)
#     posted_to = models.ManyToOneRel(Profile)
#     message = models.CharField(max_length=140)
#     posted_at = models.DateTimeField()
#
#     def __str__(self):
#         return ("Author: {}, Posted to: {} Message: {} Posted at: {}".
#                 format(self.author, self.posted_to, self.message, self.posted_at))


# class PostComments(models.Model):
#     author = models.ForeignKey(User)
#     wall_post = models.ManyToOneRel(WallPost)
#     comment = models.CharField(max_length=250)
#     posted_at = models.DateTimeField()
#
#     def __str__(self):
#         return ("Author: {}, Wall Post: {} Comment: {} Posted at: {}".
#                 format(self.author, self.wall_post, self.comment, self.posted_at))
