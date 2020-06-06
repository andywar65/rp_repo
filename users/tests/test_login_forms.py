from django.test import TestCase

from users.models import User

class UserLoginFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='happyparent',
            password='P4s5W0r6' )
        user2 = User.objects.create_user(username='sneakychild',
            password='P4s5W0r6', is_active=True )
        profile = user2.profile
        profile.sector = '1-YC'
        profile.parent = user
        profile.save()

    def test_auth_form_status_code(self):
        response = self.client.post('/accounts/login/',
            {'username': 'sneakychild', 'password': 'P4s5W0r6'})
        self.assertEqual(response.status_code, 200)

    def test_auth_form_clean(self):
        """
        Here we test a clean method in a front end form. Note in the assertEqual
        we get the code of the first validation error of form non field errors.
        Note that non_field_errors is a method.
        """
        response = self.client.post('/accounts/login/',
            {'username': 'sneakychild', 'password': 'P4s5W0r6'})
        self.assertEqual(response.context['form'].non_field_errors().as_data()[0].code,
            'minor_no_login')
