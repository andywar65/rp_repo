from django.test import TestCase
from django.urls import reverse

from taggit.models import Tag

from users.models import User, Profile
from cronache.models import Event, Location

class LocationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        tag = Tag.objects.create( name='bar' )
        usr = User.objects.create_user(username='event_uploader',
            password='P4s5W0r6')
        profile = Profile.objects.get(pk=usr.id)
        profile.is_trusted = True
        profile.save()
        User.objects.create_user(username='event_untrusted', password='P4s5W0r6')
        location = Location.objects.create(title='Where again', address='Mean St.',
            gmap_embed='http')
        event = Event.objects.create(title='Birthday party',
            date='2020-05-10 15:53:00+02', location=location)
        event.tags.add('bar')

    def test_locations_list_view_status_code(self):
        response = self.client.get(reverse('locations:locations'))
        self.assertEqual(response.status_code, 200)

    def test_locations_list_view_template(self):
        response = self.client.get(reverse('locations:locations'))
        self.assertTemplateUsed(response, 'cronache/location_list.html')

    def test_locations_list_view_context_object(self):
        all_locations = Location.objects.all()
        response = self.client.get(reverse('locations:locations'))
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(response.context['all_locations'],
            all_locations, transform=lambda x: x)

    def test_locations_detail_view_status_code(self):
        response = self.client.get(reverse('locations:location',
            kwargs={'slug': 'where-again'}))
        self.assertEqual(response.status_code, 200)

    def test_locations_detail_view_template(self):
        response = self.client.get(reverse('locations:location',
            kwargs={'slug': 'where-again'}))
        self.assertTemplateUsed(response, 'cronache/location_detail.html')

    def test_locations_detail_view_context_object(self):
        location = Location.objects.get(slug='where-again')
        response = self.client.get(reverse('locations:location',
            kwargs={'slug': 'where-again'}))
        self.assertEqual(response.context['location'], location )

    def test_event_archive_index_view_status_code(self):
        response = self.client.get(reverse('chronicles:event_index'))
        self.assertEqual(response.status_code, 200)

    def test_event_archive_index_view_template(self):
        response = self.client.get(reverse('chronicles:event_index'))
        self.assertTemplateUsed(response, 'cronache/event_archive.html')

    def test_event_archive_index_view_context_object(self):
        all_events = Event.objects.all()
        response = self.client.get(reverse('chronicles:event_index'))
        self.assertQuerysetEqual(response.context['all_events'],
            all_events, transform=lambda x: x)

    def test_event_archive_index_view_context_object_tagged(self):
        all_events = Event.objects.filter( tags__name='bar' )
        response = self.client.get('/calendario/?categoria=bar')
        self.assertQuerysetEqual(response.context['all_events'],
            all_events, transform=lambda x: x)

    def test_event_year_archive_view_status_code(self):
        response = self.client.get(reverse('chronicles:event_year',
            kwargs={'year': 2020}))
        self.assertEqual(response.status_code, 200)

    def test_event_year_archive_view_template(self):
        response = self.client.get(reverse('chronicles:event_year',
            kwargs={'year': 2020}))
        self.assertTemplateUsed(response, 'cronache/event_archive_year.html')

    def test_event_year_archive_view_context_object(self):
        all_events = Event.objects.filter(date__year=2020)
        response = self.client.get(reverse('chronicles:event_year',
            kwargs={'year': 2020}))
        self.assertQuerysetEqual(response.context['all_events'], all_events,
            transform=lambda x: x)

    def test_event_month_archive_view_status_code(self):
        response = self.client.get(reverse('chronicles:event_month',
            kwargs={'year': 2020, 'month': 5}))
        self.assertEqual(response.status_code, 200)

    def test_event_month_archive_view_template(self):
        response = self.client.get(reverse('chronicles:event_month',
            kwargs={'year': 2020, 'month': 5}))
        self.assertTemplateUsed(response, 'cronache/event_archive_month.html')

    def test_event_month_archive_view_context_object(self):
        all_events = Event.objects.filter(date__year=2020, date__month=5)
        response = self.client.get(reverse('chronicles:event_month',
            kwargs={'year': 2020, 'month': 5}))
        self.assertQuerysetEqual(response.context['all_events'], all_events,
            transform=lambda x: x)

    def test_event_day_archive_view_status_code(self):
        response = self.client.get(reverse('chronicles:event_day',
            kwargs={'year': 2020, 'month': 5, 'day': 10}))
        self.assertEqual(response.status_code, 200)

    def test_event_day_archive_view_template(self):
        response = self.client.get(reverse('chronicles:event_day',
            kwargs={'year': 2020, 'month': 5, 'day': 10}))
        self.assertTemplateUsed(response, 'cronache/event_archive_day.html')

    def test_event_day_archive_view_context_object(self):
        all_events = Event.objects.filter(date__year=2020, date__month=5,
            date__day=10)
        response = self.client.get(reverse('chronicles:event_day',
            kwargs={'year': 2020, 'month': 5, 'day': 10}))
        self.assertQuerysetEqual(response.context['all_events'], all_events,
            transform=lambda x: x)

    def test_event_detail_view_status_code(self):
        response = self.client.get(reverse('chronicles:event_detail',
            kwargs={'year': 2020, 'month': 5, 'day': 10, 'slug': 'birthday-party'}))
        self.assertEqual(response.status_code, 200)

    def test_event_detail_view_template(self):
        response = self.client.get(reverse('chronicles:event_detail',
            kwargs={'year': 2020, 'month': 5, 'day': 10, 'slug': 'birthday-party'}))
        self.assertTemplateUsed(response, 'cronache/event_detail.html')

    def test_event_detail_view_context_object(self):
        event = Event.objects.get(slug='birthday-party')
        response = self.client.get(reverse('chronicles:event_detail',
            kwargs={'year': 2020, 'month': 5, 'day': 10, 'slug': 'birthday-party'}))
        self.assertEqual(response.context['event'], event )

    def test_user_upload_create_view_redirect_not_logged(self):
        event = Event.objects.get(slug='birthday-party')
        response = self.client.get(f'/calendario/contributi/?event_id={event.id}')
        self.assertRedirects(response,
            f'/accounts/login/?next=/calendario/contributi/%3Fevent_id%3D{event.id}')

    def test_user_upload_create_view_status_code(self):
        self.client.post('/accounts/login/', {'username':'event_uploader',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('chronicles:event_upload'))
        self.assertEqual(response.status_code, 200)

    def test_user_upload_create_view_untrusted_status_code(self):
        self.client.post('/accounts/login/', {'username':'event_untrusted',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('chronicles:event_upload'))
        self.assertEqual(response.status_code, 404)

    def test_user_upload_create_view_template(self):
        self.client.post('/accounts/login/', {'username':'event_uploader',
            'password':'P4s5W0r6'})
        response = self.client.get(reverse('chronicles:event_upload'))
        self.assertTemplateUsed(response, 'blog/userupload_form.html')

    def test_user_upload_create_view_success_url(self):
        self.client.post('/accounts/login/', {'username':'event_uploader',
            'password':'P4s5W0r6'})
        event = Event.objects.get(slug='birthday-party')
        response = self.client.post(f'/calendario/contributi/?event_id={event.id}',
            {'body': 'Foo Bar'})
        self.assertRedirects(response,
            '/calendario/2020/05/10/birthday-party/#upload-anchor')
