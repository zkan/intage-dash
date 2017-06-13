from django.test import TestCase

from ..models import Typeform


class TypeformTest(TestCase):
    def test_save_typeform(self):
        payload = {
            'http_status': 200,
            'questions': [],
            'responses': []
        }
        Typeform.objects.create(
            uid='iPMP4Y',
            payload=payload
        )

        typeform = Typeform.objects.last()

        self.assertEqual(typeform.uid, 'iPMP4Y')
        self.assertEqual(typeform.payload, payload)
