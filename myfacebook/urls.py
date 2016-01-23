"""myfacebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls.static import static
from profile.views import Home
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', 'profile.views.home', name='home'),
   url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^profile/', include('profile.urls'), name='create_user'),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^login_redirect/', 'profile.views.login_redirect', name='login_redirect'),
    url(r'^profile/(?P<profile_id>[0-9]+)/', Home.as_view(), name='profile'),
    url(r'^login/', auth_views.login,
        {'extra_context': {'next': '/'}}, name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

