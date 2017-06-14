from unittest.mock import patch

from django.test import override_settings, TestCase

from ..api import TypeformDataAPI


class TypeformDataAPITest(TestCase):
    def setUp(self):
        self.typeform_uid = 'HQxDoM'
        self.typeform_data_api = TypeformDataAPI()

    @patch('typeforms.api.requests')
    @override_settings(TYPEFORM_API_KEY='api_key_test')
    def test_get_form_data_should_call_correct_endpoint(self, mock):
        typeform_api_key = 'api_key_test'
        self.typeform_data_api.get_form_data(self.typeform_uid)

        expected_url = f'https://api.typeform.com/v1/form/' \
            f'{self.typeform_uid}?key={typeform_api_key}'
        mock.get.assert_called_once_with(expected_url)

    @patch('typeforms.api.requests')
    def test_get_form_data_should_return_response_in_json(self, mock):
        expected = {'http_status': 200}
        mock.get.return_value.json.return_value = expected
        results = self.typeform_data_api.get_form_data(self.typeform_uid)
        self.assertDictEqual(results, expected)
