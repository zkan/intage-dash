from unittest.mock import patch

from django.test import TestCase

from ..models import Typeform


class TypeformSyncView(TestCase):
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
                    'completed': '1',
                },
                {
                    'answers': {'rating_53456466': '2'},
                    'completed': '1',
                }
            ],
            'stats': {
                'responses': {
                    'completed': 2, 'showing': 2, 'total': 2
                }
            }
        }
        Typeform.objects.create(
            uid=self.typeform_uid,
            payload={'data': ''}
        )
        self.url = f'/typeforms/{self.typeform_uid}/sync/'

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
    def test_sync_view_should_save_typeform_persistently(self, mock):
        mock.return_value.get_form_data.return_value = self.results
        self.client.get(self.url)

        typeforms = Typeform.objects.get(uid=self.typeform_uid)

        self.assertDictEqual(typeforms.payload, self.results)
