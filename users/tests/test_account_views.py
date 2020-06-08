from django.test import TestCase
from django.urls import reverse

from users.models import User

class AccountViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user0 = User.objects.create_user(username='user_0',
            password='P4s5W0r6', email='me@existing.com')
        profile = user0.profile
        profile.sector = '0-NO'
        profile.is_trusted = True
        profile.save()
        untrusty = User.objects.create_user(username='untrusty',
            password='P4s5W0r6', email='me@existing.com')
        profile = untrusty.profile
        profile.sector = '3-FI'
        profile.is_trusted = False
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
