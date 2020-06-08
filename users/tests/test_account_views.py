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
        user1 = User.objects.create_user(username='user_1',
            password='P4s5W0r6')
        profile = user1.profile
        profile.sector = '1-YC'
        profile.save()
        user2 = User.objects.create_user(username='user_2',
            password='P4s5W0r6', email='user_two@example.com')
        profile = user2.profile
        profile.sector = '2-NC'
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

    def test_template_account_view_status_code_sector_1(self):
        self.client.post('/accounts/login/', {'username':'user_1',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200 )

    def test_template_account_view_template_sector_1(self):
        self.client.post('/accounts/login/', {'username':'user_1',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'users/account_1.html' )

    def test_template_account_view_status_code_sector_2(self):
        self.client.post('/accounts/login/', {'username':'user_2',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200 )

    def test_template_account_view_template_sector_2(self):
        self.client.post('/accounts/login/', {'username':'user_2',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'users/account_2.html' )

    def test_profile_change_view_not_logged(self):
        user = User.objects.get(username='user_2')
        response = self.client.get(reverse('profile_change',
            kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 302 )

    def test_profile_change_view_not_logged_redirects(self):
        user = User.objects.get(username='user_2')
        response = self.client.get(reverse('profile_change',
            kwargs={'pk': user.id}))
        self.assertRedirects(response,
            f'/accounts/login/?next=/accounts/profile/{user.id}/change/' )

    def test_profile_change_view_404_wrong_id(self):
        user = User.objects.get(username='user_2')
        self.client.post('/accounts/login/', {'username':'user_2',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile_change', kwargs={'pk': 404}))
        self.assertEqual(response.status_code, 404 )

    def test_profile_change_view_status_code(self):
        user = User.objects.get(username='user_2')
        self.client.post('/accounts/login/', {'username':'user_2',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile_change',
            kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, 200 )

    def test_profile_change_view_template(self):
        user = User.objects.get(username='user_2')
        self.client.post('/accounts/login/', {'username':'user_2',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('profile_change',
            kwargs={'pk': user.id}))
        self.assertTemplateUsed(response, 'users/profile_change.html' )

    def test_profile_change_view_post_status_code(self):
        user = User.objects.get(username='user_2')
        self.client.post('/accounts/login/', {'username':'user_2',
            'password':'P4s5W0r6'})
        #enter all required fields!
        response = self.client.post(reverse('profile_change',
            kwargs={'pk': user.id}), {'sector': '2-NC', 'first_name': 'User',
            'last_name': 'Two', 'email': 'user_2@example.com'})
        self.assertEqual(response.status_code, 302 )

    def test_profile_change_view_post_redirects(self):
        user = User.objects.get(username='user_2')
        self.client.post('/accounts/login/', {'username':'user_2',
            'password':'P4s5W0r6'})
        response = self.client.post(reverse('profile_change',
            kwargs={'pk': user.id}), {'sector': '2-NC', 'first_name': 'User',
            'last_name': 'Two', 'email': 'user_2@example.com'})
        self.assertRedirects(response,
            '/accounts/profile/?submitted=User%20Two' )
