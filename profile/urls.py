from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from profile.views import UpdateProfile

__author__ = 'traciarms'



urlpatterns = [

    url(r'^register/', 'profile.views.create_user', name='register'),

    url(r'^update_profile/(?P<profile_id>[0-9]+)/',
        login_required(UpdateProfile.as_view()), name='update_profile'),
]