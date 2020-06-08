from django.test import TestCase
from django.urls import reverse

from users.models import User

class AccountViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user0 = User.objects.create_user(username='user_0',
            password='P4s5W0r6')
        profile = user0.profile
        profile.sector = '0-NO'
        profile.is_trusted = True
        profile.save()
        untrusty = User.objects.create_user(username='untrusty',
            password='P4s5W0r6')
        profile = untrusty.profile
        profile.sector = '3-FI'
        profile.is_trusted = False
        profile.save()
        uncomplete = User.objects.create_user(username='uncomplete',
            password='P4s5W0r6')
        profile = uncomplete.profile
        profile.sector = '3-FI'
        profile.is_trusted = True
        profile.save()
        trustyparent = User.objects.create_user(username='trustyparent',
            password='P4s5W0r6', first_name='Trusty')
        profile = trustyparent.profile
        profile.sector = '3-FI'
        profile.is_trusted = True
        profile.fiscal_code = 'GRRNDR65D13F839E'
        profile.save()

    def test_profile_add_child_view_404_sector_0(self):
        self.client.post('/accounts/login/', {'username':'user_0',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile_add_child'))
        self.assertEqual(response.status_code, 404 )

    def test_profile_add_child_view_404_untrusted(self):
        self.client.post('/accounts/login/', {'username':'untrusty',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile_add_child'))
        self.assertEqual(response.status_code, 404 )

    def test_profile_add_child_view_404_uncomplete(self):
        self.client.post('/accounts/login/', {'username':'uncomplete',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile_add_child'))
        self.assertEqual(response.status_code, 404 )

    def test_profile_add_child_view_status_code(self):
        self.client.post('/accounts/login/', {'username':'trustyparent',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile_add_child'))
        self.assertEqual(response.status_code, 200 )

    def test_profile_add_child_view_template(self):
        self.client.post('/accounts/login/', {'username':'trustyparent',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile_add_child'))
        self.assertTemplateUsed(response, 'users/profile_add_child.html' )

    def test_profile_add_child_view_post_status_code(self):
        self.client.post('/accounts/login/', {'username':'trustyparent',
            'password':'P4s5W0r6'})
        response = self.client.post(reverse('profile_add_child'),
            {'first_name': 'Child', 'last_name': 'Trusty'})
        self.assertEqual(response.status_code, 302 )

    def test_profile_add_child_view_post_redirects(self):
        self.client.post('/accounts/login/', {'username':'trustyparent',
            'password':'P4s5W0r6'})
        response = self.client.post(reverse('profile_add_child'),
            {'first_name': 'Child', 'last_name': 'Trusty'})
        self.assertRedirects(response, '/accounts/profile/?child_created=True' )
