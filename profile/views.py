from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, UpdateView
from profile.forms import ProfileCreationForm, ProfileForm
from profile.models import Profile

__author__ = 'traciarms'


def create_user(request):
    if request.method == "POST":
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = form.save()
            profile = Profile()
            profile.user = user
            profile.dob = data['dob']
            profile.gender = data['gender']
            profile.phone = data['phone']
            profile.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            login(request, user)

            return HttpResponseRedirect(reverse('home'))
    else:
        form = ProfileCreationForm()

    return render(request, 'profile_registration.html',
                  {'form': form})

def login_redirect(request):
    user = request.user
    if hasattr(user, 'profile') and user.profile.id > 0:
        return HttpResponseRedirect(reverse('profile',
                                            args=[user.profile.id]))
    else:
        return HttpResponseRedirect(reverse('home'))


class Home(ListView):
    model = Profile
    template_name = "profile.html"
    queryset = Profile.objects.all()
    context_object_name = 'profile'


class UpdateProfile(UpdateView):
    model = Profile
    form_class = ProfileForm
    pk_url_kwarg = 'profile_id'
    template_name = "update_profile.html"

    def get_success_url(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
        return reverse('profile', kwargs={'profile_id': profile.id})

    def form_valid(self, form):
        profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
        user = profile.user
        user.first_name = form.cleaned_data.get('first_name', None)
        user.last_name = form.cleaned_data.get('last_name', None)
        user.email = form.cleaned_data.get('email', None)
        user.save()
        return super(UpdateProfile, self).form_valid(form)

    def get_initial(self):
        profile = Profile.objects.get(pk=self.kwargs.get('profile_id', None))
        return {'first_name': profile.user.first_name,
                'last_name': profile.user.last_name,
                'email': profile.user.email}

