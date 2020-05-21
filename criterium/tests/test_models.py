from django.test import TestCase

from users.models import User, Profile
from cronache.models import Event
from criterium.models import Race, Athlete

class RaceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='juantorena',
            password='P4s5W0r6' )
        profile = Profile.objects.get(pk=user.id)
        profile.gender = 'M'
        profile.sector = '2-NC'
        profile.save()
        event = Event.objects.create(title='Race event',
            date = '2020-05-10 15:53:00+02',
            )
        Race.objects.create(title='Race 1', event=event)
        Race.objects.create(title='Race 2', date='2020-05-11')

    def test_race_get_date(self):
        race = Race.objects.get(slug='race-2')
        self.assertEquals(race.get_date(), race.date)

    def test_race_get_date_from_event(self):
        race = Race.objects.get(slug='race-1')
        self.assertEquals(race.get_date(), race.event.date.date())
