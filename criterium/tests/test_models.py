from django.test import TestCase

from users.models import User, Profile
from cronache.models import Event, Location
from criterium.models import Race, Athlete

class RaceModelTest(TestCase):
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

    def test_race_get_date(self):
        race = Race.objects.get(slug='race-2')
        self.assertEquals(race.get_date(), race.date)

    def test_race_get_date_from_event(self):
        race = Race.objects.get(slug='race-1')
        self.assertEquals(race.get_date(), race.event.date.date())

    def test_race_get_edition(self):
        race = Race.objects.get(slug='race-2')
        self.assertEquals(race.get_edition(), '2020-2021')

    def test_race_get_edition_from_event(self):
        race = Race.objects.get(slug='race-1')
        self.assertEquals(race.get_edition(), '2019-2020')

    def test_race_get_path(self):
        race = Race.objects.get(slug='race-2')
        self.assertEquals(race.get_path(), '/criterium/2020-2021/race-2')

    def test_race_get_path_from_event(self):
        race = Race.objects.get(slug='race-1')
        self.assertEquals(race.get_path(), '/criterium/2019-2020/race-1')

    def test_race_get_location(self):
        location = Location.objects.get(slug='here')
        race = Race.objects.get(slug='race-2')
        self.assertEquals(race.get_location(), location)

    def test_race_get_location_from_event(self):
        location = Location.objects.get(slug='here')
        race = Race.objects.get(slug='race-1')
        self.assertEquals(race.get_location(), location)

    def test_race_str_method(self):
        race = Race.objects.get(slug='race-1')
        self.assertEquals(race.__str__(), 'Race 1')

    def test_athlete_str_method(self):
        user = User.objects.get(username='juantorena')
        athlete = Athlete.objects.get(user_id=user.id)
        self.assertEquals(athlete.__str__(), 'Alberto Juantorena')

    def test_athlete_get_full_name(self):
        user = User.objects.get(username='juantorena')
        athlete = Athlete.objects.get(user_id=user.id)
        self.assertEquals(athlete.get_full_name(), 'Alberto Juantorena')
