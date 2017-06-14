from unittest.mock import patch

from django.test import TestCase

from ..api import TypeformDataAPI


class TypeformDataAPITest(TestCase):
    @patch('typeforms.api.requests')
    def test_get_form_data_should_call_correct_endpoint(self, mock):
        typeform_uid = 'HQxDoM'
        typeform_api_key = 'api_key_test'

        typeform_data_api = TypeformDataAPI()
        typeform_data_api.get_form_data(typeform_uid)

        expected_url = f'https://api.typeform.com/v1/form/' \
            f'{typeform_uid}?key={typeform_api_key}'
        mock.get.assert_called_once_with(expected_url)
