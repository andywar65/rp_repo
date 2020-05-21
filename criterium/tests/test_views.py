from django.test import TestCase

from users.models import User, Profile
from cronache.models import Event, Location
from criterium.models import Race, Athlete

class RaceViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='juantorena',
            first_name = 'Alberto', last_name = 'Juantorena',
            password='P4s5W0r6' )
        profile = Profile.objects.get(pk=user.id)
        profile.gender = 'M'
        profile.sector = '2-NC'
        profile.save()
        location = Location.objects.create(title='Here', address='Nowhere St.',
            gmap_embed = 'http')
        event = Event.objects.create(title='Race event',
            date = '2020-05-10 15:53:00+02', location = location
            )
        race = Race.objects.create(title='Race 1', event=event)
        Race.objects.create(title='Race 2', date='2020-12-11',
            location = location)
        Athlete.objects.create(user=user, race=race, points=1)
