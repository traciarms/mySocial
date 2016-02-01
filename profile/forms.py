from django.forms import ModelForm
from profile.models import WallPost, PostComment, Image, Profile

__author__ = 'traciarms'
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    dob = forms.CharField(max_length=10)
    gender = forms.CharField(max_length=1)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'dob', 'gender', 'phone')


class ProfileSearchForm(ModelForm):
    name = forms.CharField(label="Search for other profiles:", max_length=250)

    class Meta:
        model = User
        fields = ('name', )


class WallPostForm(ModelForm):
    message = forms.CharField(label='What\'s on your mind', max_length=250)

    class Meta:
        model = WallPost
        fields = ('message', )


class CommentForm(ModelForm):
    comment = forms.CharField(label='Comment on this post', max_length=250)

    class Meta:
        model = PostComment
        fields = ('comment', )


class UploadImageForm(forms.Form):
    image = forms.ImageField()

    class Meta:
        model = Image
        fields = ('image', )


class UpdateProfileImgForm(ModelForm):
    image_id = forms.IntegerField(required=True, error_messages={'required': 'Please click on an image to select '
                                                                             'and then click Change Profile Photo button.'})

    class Meta:
        model = Profile
        fields = ('image_id', )
