from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Typeform
from form_submissions.models import FormResponse


class TypeformSyncViewTest(TestCase):
    def setUp(self):
        self.typeform_uid = 'HQxDoM'
        self.results = {
            'http_status': 200,
            'questions': [
                {
                    'field_id': 53456466,
                    'id': 'rating_53456466',
                    'question': 'Give me some rate.'
                }
            ],
            'responses': [
                {
                    'answers': {'rating_53456466': '3'},
                    'token': '99a9beebfe0bc18e0d95a8aexe670cd6',
                    'completed': '1',
                },
                {
                    'answers': {'rating_53456466': '2'},
                    'token': '46a9beebfe0bc18e0d95a8aeb0670cd6',
                    'completed': '1',
                }
            ],
            'stats': {
                'responses': {
                    'completed': 2,
                    'showing': 2,
                    'total': 2
                }
            }
        }
        Typeform.objects.create(
            uid=self.typeform_uid,
            payload={'data': ''}
        )
        self.url = reverse(
            'typeform_sync',
            kwargs={
                'typeform_uid': self.typeform_uid
            }
        )

    @patch('typeforms.views.TypeformDataAPI')
    def test_sync_view_should_be_accessible(self, mock):
        mock.return_value.get_form_data.return_value = self.results
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @patch('typeforms.views.TypeformDataAPI')
    def test_sync_view_should_call_get_form_data(self, mock):
        mock.return_value.get_form_data.return_value = self.results
        self.client.get(self.url)
        mock.return_value.get_form_data.assert_called_once_with(
            self.typeform_uid
        )

    @patch('typeforms.views.TypeformDataAPI')
    def test_sync_view_should_save_typeform_payload_persistently(self, mock):
        mock.return_value.get_form_data.return_value = self.results
        self.client.get(self.url)

        typeform = Typeform.objects.get(uid=self.typeform_uid)

        self.assertDictEqual(typeform.payload, self.results)

    @patch('typeforms.views.TypeformDataAPI')
    def test_sync_view_should_save_answers_persistently(self, mock):
        payload = {
            'responses': [
                {
                    'answers': {
                        'list_53368385_choice': 'BKK',
                        'rating_53368555': '7',
                    },
                    'token': 'a3e7d92cb286fd9257e3a8c309495d1f'
                },
                {
                    'answers': {
                        'list_53368385_choice': 'Nonthaburi',
                        'rating_53368555': '5',
                    },
                    'token': '46a9beebfe0bc18e0d95a8aeb0670cd6'
                }
            ]
        }
        mock.return_value.get_form_data.return_value = payload
        self.client.get(self.url)

        typeform = Typeform.objects.get(uid=self.typeform_uid)
        form_responses = FormResponse.objects.filter(
            typeform=typeform
        ).order_by('id')

        self.assertEqual(len(form_responses), 2)

        expected_answers = {
            'list_53368385_choice': 'BKK',
            'rating_53368555': 7,
        }
        expected_token = 'a3e7d92cb286fd9257e3a8c309495d1f'
        self.assertDictEqual(form_responses[0].answers, expected_answers)
        self.assertEqual(form_responses[0].token, expected_token)

        expected_answers = {
            'list_53368385_choice': 'Nonthaburi',
            'rating_53368555': 5,
        }
        expected_token = '46a9beebfe0bc18e0d95a8aeb0670cd6'
        self.assertDictEqual(form_responses[1].answers, expected_answers)
        self.assertEqual(form_responses[1].token, expected_token)

    @patch('typeforms.views.TypeformDataAPI')
    def test_sync_view_should_not_save_answer_if_get_same_token(self, mock):
        payload = {
            'responses': [
                {
                    'answers': {
                        'list_53368385_choice': 'BKK',
                        'rating_53368555': '7',
                    },
                    'token': 'a3e7d92cb286fd9257e3a8c309495d1f'
                },
                {
                    'answers': {
                        'list_53368385_choice': 'BKK',
                        'rating_53368555': '7',
                    },
                    'token': 'a3e7d92cb286fd9257e3a8c309495d1f'
                }
            ]
        }
        mock.return_value.get_form_data.return_value = payload
        self.client.get(self.url)

        typeform = Typeform.objects.get(uid=self.typeform_uid)
        form_responses = FormResponse.objects.filter(
            typeform=typeform
        ).order_by('id')

        self.assertEqual(len(form_responses), 1)

        expected_answers = {
            'list_53368385_choice': 'BKK',
            'rating_53368555': 7,
        }
        expected_token = 'a3e7d92cb286fd9257e3a8c309495d1f'
        self.assertDictEqual(form_responses[0].answers, expected_answers)
        self.assertEqual(form_responses[0].token, expected_token)
