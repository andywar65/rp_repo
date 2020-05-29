from django.test import TestCase

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
