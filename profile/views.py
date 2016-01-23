from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, UpdateView
from profile.forms import ProfileCreationForm, ProfileForm, UploadImageForm, \
    CommentForm, WallPostForm, ProfileSearchForm, UpdateProfileImgForm
from profile.models import Profile, Image, WallPost, PostComment

__author__ = 'traciarms'


def login_redirect(request):
    user = request.user
    if hasattr(user, 'profile') and user.profile.id > 0:
        return HttpResponseRedirect(reverse('profile',
                                            args=[user.profile.id]))
    else:
        return HttpResponseRedirect(reverse('home'))


def create_user(request):
    if request.method == "POST":
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if request.user.is_authenticated():
                user = request.user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                # username = request.POST['username']
                # password = request.POST['password1']
                # user = authenticate(username=username, password=password)
                # user.authenticate()
            else:
                user = form.save()
            profile = Profile()
            profile.user = user
            user.email = data['email']
            profile.dob = data['dob']
            profile.gender = data['gender']
            profile.phone = data['phone']
            profile.save()
            user.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            login(request, user)

            return HttpResponseRedirect(reverse('home'))
    else:
        if request.user:
            user = request.user
            context = {}
            context['username'] = user.username
            context['first_name'] = user.first_name
            context['last_name'] = user.last_name
            context['email'] = user.email

        form = ProfileCreationForm(context)

    return render(request, 'profile_registration.html', {'form': form})


class ProfileList(ListView):
    model = Profile
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


def add_wall_post(request, profile_id):
    if request.method == "POST":
        form = WallPostForm(request.POST)
        forward_template = form.data.get('forward_template')
        if form.is_valid():
            user = request.user
            profile = Profile.objects.get(pk=profile_id)
            data = form.cleaned_data
            wall_post = WallPost()
            wall_post.author = user
            wall_post.message = data['message']
            wall_post.posted_to = profile
            wall_post.posted_at = datetime.now()
            wall_post.save()

            if 'home' not in forward_template:
                return HttpResponseRedirect(reverse(forward_template,
                                                    args=[profile.id]))
            else:
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
    wall_post = WallPost.objects.get(pk=wall_post_id)
    profile = Profile.objects.get(wallpost=wall_post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        forward_template = form.data.get('forward_template')
        if form.is_valid():
            data = form.cleaned_data
            comment = PostComment()

            comment.author = user
            comment.comment = data['comment']
            comment.wall_post = wall_post
            comment.posted_at = datetime.now()
            comment.save()

            if 'home' not in forward_template:
                return HttpResponseRedirect(reverse(forward_template,
                                                    args=[profile.id]))
            else:
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
            return HttpResponseRedirect(reverse('upload_image'))
    else:
        form = UploadImageForm()
    return render_to_response('upload_image.html',
                              RequestContext(request, {'form': form}))


def update_profile_image(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateProfileImgForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            image = Image.objects.get(pk=data['image_id'])
            profile = user.profile
            profile.profile_thumbnail = image.image.url
            profile.save()
            return HttpResponseRedirect(reverse('profile',
                                                args=[user.profile.id]))
    else:
        form = UploadImageForm()
    return render_to_response('upload_image.html',
                              RequestContext(request, {'form': form}))


class ViewImages(ListView):
    model = Image
    template_name = "view_images.html"
    queryset = Image.objects.all()


class ViewOtherProfile(ListView):
    model = Profile
    template_name = "other_profile.html"
    pk_url_kwarg = 'profile_id'

    def get_context_data(self, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
        context = super(ViewOtherProfile, self).get_context_data(**kwargs)
        context['wall_post_list'] = profile.wallpost_set.all()
        context['form1'] = WallPostForm()
        context['form2'] = CommentForm()
        context['search_form'] = ProfileSearchForm()
        context['profile'] = profile
        return context

    def get_success_url(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
        return reverse('other_profile', kwargs={'profile_id': profile.id})


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
