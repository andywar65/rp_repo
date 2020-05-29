from django.test import TestCase
from django.urls import reverse

from cronache.models import Location
from .models import Convention, Society

class ConventionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        location = Location.objects.create(title='Place', address='Nowhere St.',
            gmap_embed = 'http')
        Convention.objects.create(title='Doctor Who', location=location)
        Society.objects.create(title='Rif Pod', denomination='ASD')

    def test_convention_model_str_method(self):
        convention = Convention.objects.get(slug='doctor-who')
        self.assertEqual(convention.__str__(), 'Doctor Who')

    def test_convention_model_get_location(self):
        location = Location.objects.get(slug='place')
        convention = Convention.objects.get(slug='doctor-who')
        self.assertEqual(convention.get_location(), location)

    def test_convention_model_get_path(self):
        convention = Convention.objects.get(slug='doctor-who')
        self.assertEqual(convention.get_path(), '/convenzioni/doctor-who')

    def test_society_model_str_method(self):
        society = Society.objects.get(title='Rif Pod')
        self.assertEqual(society.__str__(), 'Rif Pod')

    def test_convention_list_view_status_code(self):
        response = self.client.get(reverse('conventions:index'))
        self.assertEqual(response.status_code, 200)

    def test_convention_list_view_template(self):
        response = self.client.get(reverse('conventions:index'))
        self.assertTemplateUsed(response, 'direzione/convention_list.html')

    def test_convention_list_context_object(self):
        conventions = Convention.objects.filter(slug='doctor-who')
        response = self.client.get(reverse('conventions:index'))
        #workaround found in
        #https://stackoverflow.com/questions/17685023/how-do-i-test-django-querysets-are-equal
        self.assertQuerysetEqual(response.context['all_conventions'],
            conventions, transform=lambda x: x)

    def test_convention_detail_view_status_code(self):
        response = self.client.get(reverse('conventions:detail',
            kwargs={'slug': 'doctor-who'}))
        self.assertEqual(response.status_code, 200)

    def test_convention_detail_view_template(self):
        response = self.client.get(reverse('conventions:detail',
            kwargs={'slug': 'doctor-who'}))
        self.assertTemplateUsed(response, 'direzione/convention_detail.html')

    def test_convention_detail_context_object(self):
        convention = Convention.objects.get(slug='doctor-who')
        response = self.client.get(reverse('conventions:detail',
            kwargs={'slug': 'doctor-who'}))
        self.assertEqual(response.context['conv'], convention)
