from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from profile.views import UpdateProfile, ViewImages, ProfileList

__author__ = 'traciarms'


urlpatterns = [

    url(r'^register/', 'profile.views.create_user', name='register'),

    url(r'^update_profile/(?P<profile_id>[0-9]+)/',
        login_required(UpdateProfile.as_view()), name='update_profile'),

    url(r'^upload_images/',
        'profile.views.upload_image', name='upload_image'),

    url(r'^view_images/',
        ViewImages.as_view(), name='view_images'),

    url(r'^add_wall_post/', 'profile.views.add_wall_post', name='add_wall_post'),

    url(r'^add_comment/(?P<wall_post_id>[0-9]+)/', 'profile.views.add_comment', name='add_comment'),

    url(r'^list_profiles/', ProfileList.as_view(), name='list_profiles'),
]