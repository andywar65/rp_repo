from datetime import date, timedelta

from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from users.models import User, Profile#, CourseSchedule, UserMessage

class UserAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='userchanger',
            password='P4s5W0r6', is_staff = True )
        profile = user.profile
        profile.sector = '1-YC'
        profile.mc_state = '0-NF'
        profile.med_cert = 'documents/foobar.pdf'
        profile.save()
        user2 = User.objects.create_user(username='profilechanger',
            password='P4s5W0r6', is_staff = True )
        profile = user2.profile
        profile.sector = '0-NO'
        profile.save()
        user3 = User.objects.create_user(username='staffmember',
            password='P4s5W0r6', is_staff = True )
        profile = user3.profile
        profile.sector = '2-NC'
        profile.mc_state = '2-RE'
        profile.mc_expiry = date.today() + timedelta(days=15)
        profile.save()
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(
            codename='change_user',
            content_type=content_type,
        )
        user.user_permissions.add(permission)
        content_type = ContentType.objects.get_for_model(Profile)
        permission = Permission.objects.get(
            codename='view_profile',
            content_type=content_type,
        )
        user.user_permissions.add(permission)
        user2.user_permissions.add(permission)
        user4 = User.objects.create_user(username='fatparent',
            password='P4s5W0r6' )
        profile = user4.profile
        profile.sector = '3-FI'
        profile.save()
        user5 = User.objects.create_user(username='skinnychild',
            password='P4s5W0r6' )
        profile = user5.profile
        profile.sector = '1-YC'
        profile.parent = user4
        profile.save()
        user6 = User.objects.create_user(username='certexpired',
            password='P4s5W0r6' )
        profile = user6.profile
        profile.sector = '1-YC'
        profile.mc_state = '2-RE'
        profile.mc_expiry = date.today() - timedelta(days=15)
        profile.save()
        user7 = User.objects.create_user(username='anotherexpired',
            password='P4s5W0r6' )
        profile = user7.profile
        profile.sector = '1-YC'
        profile.mc_state = '6-IS'
        profile.mc_expiry = date.today() - timedelta(days=15)
        profile.save()

    #covering get queryset

    def test_profile_admin_status_code_user_changer(self):
        self.client.post('/admin/login/', {'username':'userchanger',
            'password':'P4s5W0r6'})
        response = self.client.get('/admin/users/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_admin_status_code_profile_changer(self):
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        response = self.client.get('/admin/users/profile/')
        self.assertEqual(response.status_code, 200)

    #covering change view

    def test_profile_admin_status_code_staff_member(self):
        self.client.post('/admin/login/', {'username':'staffmember',
            'password':'P4s5W0r6'})
        response = self.client.get('/admin/users/profile/')
        self.assertEqual(response.status_code, 403)#403=forbidden

    def test_profile_admin_status_code_sector_0(self):
        user = User.objects.get(username='profilechanger')
        self.client.post('/admin/login/', {'username':'userchanger',
            'password':'P4s5W0r6'})
        response = self.client.get(f'/admin/users/profile/{user.id}/change/')
        self.assertEqual(response.status_code, 200)

    def test_profile_admin_status_code_sector_1(self):
        user = User.objects.get(username='userchanger')
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        response = self.client.get(f'/admin/users/profile/{user.id}/change/')
        self.assertEqual(response.status_code, 200)

    def test_profile_admin_status_code_sector_2(self):
        user = User.objects.get(username='staffmember')
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        response = self.client.get(f'/admin/users/profile/{user.id}/change/')
        self.assertEqual(response.status_code, 200)

    def test_profile_admin_status_code_sector_3(self):
        user = User.objects.get(username='fatparent')
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        response = self.client.get(f'/admin/users/profile/{user.id}/change/')
        self.assertEqual(response.status_code, 200)

    def test_profile_admin_status_code_child(self):
        user = User.objects.get(username='skinnychild')
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        response = self.client.get(f'/admin/users/profile/{user.id}/change/')
        self.assertEqual(response.status_code, 200)

    #covering action mc state

    def test_profile_admin_control_mc_action_status_code(self):
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        users = User.objects.all().values_list('id', flat=True)
        response = self.client.post('/admin/users/profile/',
            {'action': 'control_mc', '_selected_action': users}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_admin_control_mc_action_mc_state_none(self):
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        users = User.objects.all().values_list('id', flat=True)
        response = self.client.post('/admin/users/profile/',
            {'action': 'control_mc', '_selected_action': users})
        user = User.objects.get(username='skinnychild')
        self.assertEqual(user.profile.mc_state, '0-NF')

    def test_profile_admin_control_mc_action_mc_state_0_NF(self):
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        users = User.objects.all().values_list('id', flat=True)
        response = self.client.post('/admin/users/profile/',
            {'action': 'control_mc', '_selected_action': users})
        user = User.objects.get(username='userchanger')
        self.assertEqual(user.profile.mc_state, '1-VF')

    def test_profile_admin_control_mc_action_mc_state_expired(self):
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        users = User.objects.all().values_list('id', flat=True)
        response = self.client.post('/admin/users/profile/',
            {'action': 'control_mc', '_selected_action': users})
        user = User.objects.get(username='certexpired')
        self.assertEqual(user.profile.mc_state, '3-SV')

    def test_profile_admin_control_mc_action_mc_state_to_expire(self):
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        users = User.objects.all().values_list('id', flat=True)
        response = self.client.post('/admin/users/profile/',
            {'action': 'control_mc', '_selected_action': users})
        user = User.objects.get(username='staffmember')
        self.assertEqual(user.profile.mc_state, '6-IS')

    def test_profile_admin_control_mc_action_mc_state_totally_expired(self):
        self.client.post('/admin/login/', {'username':'profilechanger',
            'password':'P4s5W0r6'})
        users = User.objects.all().values_list('id', flat=True)
        response = self.client.post('/admin/users/profile/',
            {'action': 'control_mc', '_selected_action': users})
        user = User.objects.get(username='anotherexpired')
        self.assertEqual(user.profile.mc_state, '3-SV')
