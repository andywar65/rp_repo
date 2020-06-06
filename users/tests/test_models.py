from django.test import TestCase
from django.utils.html import format_html

from users.models import User, CourseSchedule, Profile, UserMessage

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        parent = User.objects.create_user(username='rawydna56',
            password='P4s5W0r6')
        profile = parent.profile
        profile.sector = '3-FI'
        profile.date_of_birth = '1965-5-10'
        profile.mc_state = '02NI'
        profile.save()
        user = User.objects.create_user(username='andy.war65', password='P4s5W0r6',
            first_name='Andrea', last_name='Guerra', email='andy@war.com')
        #next save is just for coverage purposes
        user.save()
        profile = user.profile
        profile.avatar = 'uploads/users/avatar.jpg'
        profile.parent = parent
        profile.gender = 'M'
        profile.date_of_birth = '2010-5-10'
        profile.mc_state = '62II'
        profile.save()
        unborn = User.objects.create_user(username='unborn',
            password='P4s5W0r6')
        profile = unborn.profile
        profile.mc_state = '4-SI'
        profile.save()
        sector = User.objects.create_user(username='sector',
            password='P4s5W0r6', first_name='Sector')
        profile = sector.profile
        profile.sector = '0-NO'
        profile.save()
        fiscal = User.objects.create_user(username='fiscal',
            password='P4s5W0r6', first_name='Fiscal')
        profile = fiscal.profile
        profile.sector = '3-FI'
        profile.fiscal_code = 'GRRNDR65D13F839E'
        profile.save()
        phoney = User.objects.create_user(username='phoney',
            password='P4s5W0r6', first_name='Phoo')
        profile = phoney.profile
        profile.gender = 'M'
        profile.phone = '123456789'
        profile.save()
        CourseSchedule.objects.create(full='Foo Bar', abbrev='FB')
        UserMessage.objects.create(user=user, subject='Foo', body='Bar')
        UserMessage.objects.create(nickname='Nick Name',
            email='me@example.com', subject='Foo', body='Bar')

    def test_user_get_full_name(self):
        user = User.objects.get(username='andy.war65')
        self.assertEquals(user.get_full_name(), 'Andrea Guerra')

    def test_user_get_full_username(self):
        user = User.objects.get(username='rawydna56')
        self.assertEquals(user.get_full_name(), 'rawydna56')

    def test_user_get_short_name(self):
        user = User.objects.get(username='andy.war65')
        self.assertEquals(user.get_short_name(), 'Andrea')

    def test_user_get_short_username(self):
        user = User.objects.get(username='rawydna56')
        self.assertEquals(user.get_short_name(), 'rawydna56')

    def test_user_str_full_name(self):
        user = User.objects.get(username='andy.war65')
        self.assertEquals(user.__str__(), 'Andrea Guerra')

    def test_user_str_username(self):
        user = User.objects.get(username='rawydna56')
        self.assertEquals(user.__str__(), 'rawydna56')

    def test_user_model_get_children(self):
        user = User.objects.get(username='rawydna56')
        children = User.objects.filter(profile__parent__id=user.id)
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(user.get_children(), children,
            transform=lambda x : x)

    def test_user_model_is_adult_unborn(self):
        user = User.objects.get(username='unborn')
        self.assertFalse(user.is_adult())

    def test_user_model_is_adult_true(self):
        user = User.objects.get(username='rawydna56')
        self.assertTrue(user.is_adult())

    def test_user_model_is_adult_false(self):
        user = User.objects.get(username='andy.war65')
        self.assertFalse(user.is_adult())

    def test_course_model_str(self):
        course = CourseSchedule.objects.get(abbrev='FB')
        self.assertEquals(course.__str__(), 'Foo Bar')

    def test_profile_get_full_name(self):
        user = User.objects.get(username='andy.war65')
        self.assertEquals(user.profile.get_full_name(), 'Andrea Guerra')

    def test_profile_get_full_username(self):
        user = User.objects.get(username='rawydna56')
        self.assertEquals(user.profile.get_full_name(), 'rawydna56')

    def test_profile_str_full_name(self):
        user = User.objects.get(username='andy.war65')
        self.assertEquals(user.profile.__str__(), 'Andrea Guerra')

    def test_profile_str_username(self):
        user = User.objects.get(username='rawydna56')
        self.assertEquals(user.profile.__str__(), 'rawydna56')

    def test_profile_get_thumb(self):
        user = User.objects.get(username='andy.war65')
        # here extracting path from FileObject for convenience
        self.assertEquals(user.profile.get_thumb().path, 'uploads/users/avatar.jpg')

    def test_profile_get_no_thumb(self):
        user = User.objects.get(username='rawydna56')
        self.assertEquals(user.profile.get_thumb(), None)

    def test_profile_model_is_complete_parent_gender(self):
        user = User.objects.get(username='andy.war65')
        self.assertEquals(user.profile.is_complete(),
            format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">'))

    def test_profile_model_is_complete_sector_0(self):
        user = User.objects.get(username='sector')
        self.assertEquals(user.profile.is_complete(),
            format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">'))

    def test_profile_model_is_complete_fiscal_code(self):
        user = User.objects.get(username='fiscal')
        self.assertEquals(user.profile.is_complete(),
            format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">'))

    def test_profile_model_is_complete_phone(self):
        user = User.objects.get(username='phoney')
        self.assertEquals(user.profile.is_complete(),
            format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">'))

    def test_profile_model_is_complete_no(self):
        user = User.objects.get(username='unborn')
        self.assertEquals(user.profile.is_complete(),
            format_html('<img src="/static/admin/img/icon-no.svg" alt="False">'))

    def test_user_message_get_full_name(self):
        user = User.objects.get(username='andy.war65')
        message = UserMessage.objects.get(user = user)
        self.assertEquals(message.get_full_name(), 'Andrea Guerra')

    def test_user_message_get_nickname(self):
        message = UserMessage.objects.get(nickname = 'Nick Name')
        self.assertEquals(message.get_full_name(), 'Nick Name')

    def test_user_message_get_user_email(self):
        user = User.objects.get(username='andy.war65')
        message = UserMessage.objects.get(user = user)
        self.assertEquals(message.get_email(), 'andy@war.com')

    def test_user_message_get_nickname_email(self):
        message = UserMessage.objects.get(nickname = 'Nick Name')
        self.assertEquals(message.get_email(), 'me@example.com')

    def test_user_message_str_method(self):
        user = User.objects.get(username='andy.war65')
        message = UserMessage.objects.get(user = user)
        self.assertEquals(message.__str__(), f'Messaggio - {message.id}')
