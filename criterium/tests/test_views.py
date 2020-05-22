from datetime import datetime

from django.test import TestCase
from django.urls import reverse

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

    def test_race_redirect_view_status_code(self):
        response = self.client.get('/criterium/')
        self.assertEqual(response.status_code, 302)

    def test_race_redirect_view_redirects(self):
        response = self.client.get('/criterium/')
        date = datetime.now()
        year = date.year
        month = date.month
        if month >= 11:
            self.assertRedirects(response,
                f'/criterium/{year}-{year+1}/')
        else:
            self.assertRedirects(response,
                f'/criterium/{year-1}-{year}/')

    def test_correct_redirect_view_status_code(self):
        response = self.client.get(reverse('criterium:correct_edition',
            kwargs={'year': 2019}))
        self.assertEqual(response.status_code, 302)

    def test_correct_redirect_view_redirects(self):
        response = self.client.get(reverse('criterium:correct_edition',
            kwargs={'year': 2019}))
        self.assertRedirects(response, '/criterium/2019-2020/')

    def test_race_list_view_status_code(self):
        response = self.client.get('/criterium/2019-2020/')
        self.assertEqual(response.status_code, 200)

    def test_race_list_view_template(self):
        response = self.client.get('/criterium/2019-2020/')
        self.assertTemplateUsed(response, 'criterium/race_list.html')

    def test_race_list_view_context_races(self):
        all_races = Race.objects.filter(slug='race-1')
        response = self.client.get('/criterium/2019-2020/')
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(response.context['all_races'], all_races,
            transform=lambda x: x)

    def test_race_list_view_context_females(self):
        response = self.client.get('/criterium/2019-2020/')
        self.assertEqual(response.context['females'], {})

    def test_race_list_view_context_males(self):
        race = Race.objects.get(slug='race-1')
        user = User.objects.get(username='juantorena')
        athlete = Athlete.objects.get(user=user, race=race)
        response = self.client.get('/criterium/2019-2020/')
        self.assertEqual(response.context['males'],
            {athlete.id: ('Alberto Juantorena', 1)})

    def test_race_list_view_context_status(self):
        #this test will fail in a hundred years
        response = self.client.get('/criterium/2119-2120/')
        self.assertEqual(response.context['status'], 'provvisoria')

    def test_race_list_view_context_status(self):
        response = self.client.get('/criterium/2018-2019/')
        self.assertEqual(response.context['status'], 'definitiva')

    def test_race_detail_view_status_code(self):
        response = self.client.get('/criterium/2019-2020/race-1/')
        self.assertEqual(response.status_code, 200)

    def test_race_detail_view_status_code_not_found(self):
        #we have to control this
        response = self.client.get('/criterium/2019-2020/race-2/')
        self.assertEqual(response.status_code, 404)

    def test_race_detail_view_template(self):
        response = self.client.get('/criterium/2019-2020/race-1/')
        self.assertTemplateUsed(response, 'criterium/race_detail.html')
