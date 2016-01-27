from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from profile.forms import ProfileCreationForm, UploadImageForm
from profile.models import Profile, PostComment, WallPost, Image

__author__ = 'traciarms'


class UserViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.test_user.save()
        self.profile = Profile.objects.create(user=self.test_user)
        self.profile.save()

    def test_create_user(self):
        self.client.login(username='test', password='pass')
        resp = self.client.get(reverse('profile', args=[self.profile.id]))
        self.assertEqual(resp.status_code, 200)


class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
                username='tracia',
                first_name='traci',
                last_name='armstrong',
                email='test@test.com'
        )
        self.client.force_login(user=self.user)
        self.profile = Profile.objects.create(
            user=self.user,
            dob='08-08-1980',
            gender='F',
            phone='321-863-1233'
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)

    def test_update_profile(self):
        resp = self.client.get(reverse('update_profile', kwargs={'profile_id':self.profile.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'update_profile.html')

    def test_view_other_profile(self):
        resp = self.client.get(reverse('other_profile', args=[self.profile.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'other_profile.html')

    def test_update_profile_image(self):
        resp = self.client.get(reverse('update_profile_image'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'upload_image.html')

    def test_profile_list_view(self):
        resp = self.client.get(reverse('list_profiles'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'list_profiles.html')


class ImageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
                username='tracia'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            dob='08-08-1980',
            gender='F',
            phone='321-123-1234'
        )
        self.client.force_login(user=self.user)

    def test_image_creation(self):
        image = Image.objects.create(
            profile=self.profile
        )

        self.assertEqual(image.profile, self.profile)

    def test_upload_image(self):
        resp = self.client.get(reverse('upload_image'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'upload_image.html')

    def test_view_image(self):
        resp = self.client.get(reverse('view_images'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'view_images.html')


class WallPostTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tracia'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            dob='08-08-1980',
            gender='F',
            phone='321-123-1234'
        )
        self.now = datetime.now()
        wall_post = WallPost.objects.create(
            author=self.user,
            posted_to=self.profile,
            message='this is my message',
            posted_at=self.now
        )
        self.client.force_login(user=self.user)

    def test_wall_post_creation(self):
        self.assertEqual(self.wall_post.posted_at, self.now)

    def test_add_wall_post(self):
        resp = self.client.get(reverse('add_wall_post',
                                       kwargs={'profile_id': self.profile.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'profile.html')

class PostCommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.user.save()
        self.profile = Profile.objects.create(user=self.user)
        self.profile.save()
        self.wall_post = WallPost.objects.create(
            author=self.user,
            posted_to=self.profile,
            message='My message',
            posted_at=datetime.now()
        )
        self.client.force_login(user=self.user)

    def test_post_comment_creation(self):
        now = datetime.now()
        post_comment = PostComment.objects.create(
            author=self.user,
            wall_post=self.wall_post,
            comment='this is my message',
            posted_at=now
        )

        self.assertEqual(post_comment.posted_at, now)

    def test_add_comment(self):
        resp = self.client.get(reverse('add_comment',
                                       kwargs={'wall_post_id': self.wall_post.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'profile.html')


class ProfileCreationFormTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('traciarms')
        self.profile = Profile.objects.create(user=user, dob='08-08-1987',
                                              gender='F', phone='321-863-1111')

    def test_valid_data(self):
        form = ProfileCreationForm({
            'username': 'traci111',
            'first_name': 'Traci',
            'last_name': 'Armstrong',
            'email': 'test@test.com',
            'dob': '08-08-1980',
            'gender': 'F',
            'phone': '321-123-1234',
            'password1': 'pass',
            'password2': 'pass'
        })
        self.assertTrue(form.is_valid())
        profile = form.save()
        self.assertEqual(profile.username, 'traci111')
        self.assertEqual(profile.first_name, 'Traci')
        self.assertEqual(profile.last_name, 'Armstrong')
        self.assertEqual(profile.email, 'test@test.com')
