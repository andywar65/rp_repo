from django.test import TestCase

from users.models import User, Profile, CourseSchedule

class UserFrontFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        course = CourseSchedule.objects.create(abbrev='ALT', full='Altro')
        user = User.objects.create_user(username='coursealt',
            password='P4s5W0r6', is_active=True )
        profile = user.profile
        profile.sector = '1-YC'
        profile.save()

    def test_profile_change_course_status_code(self):
        user = User.objects.get(username='coursealt')
        self.client.post('/accounts/login/', {'username': 'coursealt',
            'password': 'P4s5W0r6'})
        response = self.client.get(f'/accounts/profile/{user.id}/change/course/')
        self.assertEqual(response.status_code, 200)

    def test_profile_change_course_clean(self):
        """
        Here we test a clean method in a front end form. Note in the assertEqual
        we get the first error message of the course_alt form field. In admin
        we just have response.context.['errors']
        """
        course = CourseSchedule.objects.get(abbrev='ALT')
        user = User.objects.get(username='coursealt')
        self.client.post('/accounts/login/', {'username': 'coursealt',
            'password': 'P4s5W0r6'})
        response = self.client.post(f'/accounts/profile/{user.id}/change/course/',
            {'course': [course.id], 'course_membership': 'INTU'})
        self.assertEqual(response.context['form'].errors['course_alt'][0],
            "Hai scelto 'Altro', quindi scrivi qualcosa!")
