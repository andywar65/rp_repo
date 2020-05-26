from django.test import TestCase
from django.utils.timezone import now

#from users.models import User, Profile
from cronache.models import Event, Location
#from criterium.models import Race, Athlete

class LocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Location.objects.create(title='Here', address='Nowhere St.',
            gmap_embed = 'http')
        Location.objects.create(title='There', address='Somewhere St.',
            gmap_embed = '<iframe src="http://foo.bar"></iframe>',
            gmap_link = 'http://foo.bar')

    def test_location_model_str_method(self):
        location = Location.objects.get(slug='here')
        self.assertEqual(location.__str__(), 'Here')

    def test_location_model_get_gmap_link_none(self):
        location = Location.objects.get(slug='here')
        self.assertEqual(location.get_gmap_link(), '-')

    def test_location_model_get_gmap_link(self):
        location = Location.objects.get(slug='there')
        self.assertEqual(location.get_gmap_link(),
            '<a href="http://foo.bar" class="btn" target="_blank">Mappa</a>')

    def test_location_model_stripped_gmap_embed(self):
        location = Location.objects.get(slug='there')
        self.assertEqual(location.gmap_embed, 'http://foo.bar')

class EventModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        location = Location.objects.create(title='Here', address='Nowhere St.',
            gmap_embed = 'http')
        Event.objects.create(title='Past event',
            date = '2019-05-10 15:53:00+02', location = location
            )
        Event.objects.create(title='Future event',
            date = '2119-05-10 15:53:00+02', location = location
            )
        Event.objects.create(title='Today event', location = location
            )

    def test_event_model_str_method(self):
        event = Event.objects.get(slug='today-event')
        self.assertEqual(event.__str__(), 'Today event')

    def test_event_model_get_badge_color_past(self):
        event = Event.objects.get(slug='past-event')
        self.assertEqual(event.get_badge_color(), 'secondary')

    def test_event_model_get_badge_color_future(self):
        event = Event.objects.get(slug='future-event')
        self.assertEqual(event.get_badge_color(), 'success')

    def test_event_model_get_badge_color_today(self):
        event = Event.objects.get(slug='today-event')
        self.assertEqual(event.get_badge_color(), 'warning')
