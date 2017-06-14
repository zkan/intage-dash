from unittest.mock import patch

from django.test import TestCase

from ..models import Typeform


class TypeformSyncView(TestCase):
    def setUp(self):
        typeform_uid = 'HQxDoM'
        Typeform.objects.create(
            uid='HQxDoM',
            payload=[]
        )
        self.url = f'/typeforms/{typeform_uid}/sync/'

    @patch('typeforms.views.TypeformDataAPI')
    def test_sync_view_should_be_accessible(self, mock):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @patch('typeforms.views.TypeformDataAPI')
    def test_sync_view_should_call_get_form_data(self, mock):
        response = self.client.get(self.url)
        mock.return_value.get_form_data.assert_called_once_with('HQxDoM')
