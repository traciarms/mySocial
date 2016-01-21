from django.contrib.auth import authenticate, login
from django.core.files.uploadhandler import FileUploadHandler
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, UpdateView
from myfacebook.settings import MEDIA_ROOT
from profile.forms import ProfileCreationForm, ProfileForm, UploadImageForm, \
    CommentForm, WallPostForm, ProfileSearchForm
from profile.models import Profile, Image, WallPost, PostComment

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

    return render(request, 'profile_registration.html', {'form': form})


class ProfileList(ListView):
    model = Profile
    # context_object_name = 'profiles'
    form_class = ProfileSearchForm
    template_name = 'list_profiles.html'

    def get_queryset(self):
        search_string = self.request.GET.get("name", None)
        query_set = Profile.objects.filter(Q(user__first_name__icontains=search_string) |
                                           Q(user__last_name__icontains=search_string) |
                                           Q(user__email__icontains=search_string)).all()

        return query_set


class Home(ListView):
    model = Profile
    template_name = "profile.html"
    queryset = Profile.objects.all()
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(Home, self).get_context_data(**kwargs)
        if hasattr(user, 'profile'):
            profile = self.request.user.profile
            context['wall_post_list'] = profile.wallpost_set.all()
            context['form1'] = WallPostForm()
            context['form2'] = CommentForm()
            context['search_form'] = ProfileSearchForm()
        return context


def add_wall_post(request):
    user = request.user
    if request.method == "POST":
        form = WallPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            wall_post = WallPost()
            wall_post.author = user
            wall_post.message = data['message']
            wall_post.posted_to = user.profile
            wall_post.posted_at = datetime.now()
            wall_post.save()

            return HttpResponseRedirect(reverse('home'))
    else:
        form = WallPostForm()

    form1 = WallPostForm()
    form2 = CommentForm()

    return render(request, 'profile.html', {'form': form,
                                            'form1': form1,
                                            'form2': form2})


def add_comment(request, wall_post_id):
    user = request.user
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            comment = PostComment()
            wall_post = WallPost.objects.get(pk=wall_post_id)
            comment.author = user
            comment.comment = data['comment']
            comment.wall_post = wall_post
            comment.posted_at = datetime.now()
            comment.save()

            return HttpResponseRedirect(reverse('home'))
    else:
        form = CommentForm()

    form1 = WallPostForm()
    form2 = CommentForm()

    return render(request, 'profile.html', {'form': form,
                                            'form1': form1,
                                            'form2': form2})


def upload_image(request):
    user = request.user
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            image = Image()
            image.profile = user.profile
            image.image = data['image']
            image.save()
            # FileUploadHandler(request.FILES['image'])
            # form.save()
            return HttpResponseRedirect(reverse('profile',
                                                args=[user.profile.id]))
    else:
        form = UploadImageForm()
    return render_to_response('upload_image.html',
                              RequestContext(request, {'form': form,
                                                       'MEDIA_ROOT': MEDIA_ROOT}))


class ViewImages(ListView):
    model = Image
    template_name = "view_images.html"
    queryset = Image.objects.all()


def login_redirect(request):
    user = request.user
    if hasattr(user, 'profile') and user.profile.id > 0:
        return HttpResponseRedirect(reverse('profile',
                                            args=[user.profile.id]))
    else:
        return HttpResponseRedirect(reverse('home'))


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

