from django.test import TestCase

from ..models import Typeform


class TypeformTest(TestCase):
    def setUp(self):
        self.typeform_uid = 'iPMP4Y'
        self.payload = {
            'http_status': 200,
            'questions': [],
            'responses': []
        }
        Typeform.objects.create(
            uid=self.typeform_uid,
            payload=self.payload
        )

    def test_save_typeform(self):
        typeform = Typeform.objects.last()
        self.assertEqual(typeform.uid, self.typeform_uid)
        self.assertEqual(typeform.payload, self.payload)

    def test_typeform_should_be_represented_by_uid(self):
        typeform = Typeform.objects.last()
        self.assertEqual(typeform.__str__(), 'iPMP4Y')
