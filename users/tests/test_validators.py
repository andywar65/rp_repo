from django.test import TestCase
from django.core.exceptions import ValidationError

from users.validators import validate_codice_fiscale

class ValidateCodiceFiscaleTestCase(TestCase):
    """Thanks to https://github.com/facciocose/django-italian-utils
    """
    def test_codice_fiscale_vuoto(self):
        self.assertRaises(
            ValidationError,
            validate_codice_fiscale,
            ''
        )

    def test_codice_fiscale_16(self):
        self.assertRaises(
            ValidationError,
            validate_codice_fiscale,
            '1234567890123456'
        )

    def test_codice_fiscale_controllo(self):
        self.assertRaises(
            ValidationError,
            validate_codice_fiscale,
            'ABCDEF00A00A000A'
        )

    def test_codice_fiscale_formalmente_corretto(self):
        self.assertEqual(validate_codice_fiscale('RSSMRA14M26H501N'), None)

    def test_codice_fiscale_formalmente_corretto_omocodico(self):
        self.assertEqual(validate_codice_fiscale('RSSMRA14M26H50MF'), None)
