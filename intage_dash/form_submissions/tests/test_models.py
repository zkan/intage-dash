from django.test import TestCase

from ..models import FormResponse
from typeforms.models import Typeform


class FormResponseTest(TestCase):
    def test_save_form_response(self):
        answers = [
            {
                'rating_53373838': 4,
                'rating_53368644': 8
            }
        ]
        typeform = Typeform.objects.create(
            uid='iPMP4Y',
            payload={'data': ''}
        )
        FormResponse.objects.create(
            typeform=typeform,
            answers=answers
        )

        form_response = FormResponse.objects.last()

        self.assertEqual(form_response.typeform.id, typeform.id)
        self.assertEqual(form_response.answers, answers)
