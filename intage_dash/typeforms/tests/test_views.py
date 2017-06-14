from django.test import TestCase


class TypeformSyncView(TestCase):
    def test_sync_view_should_be_accessible(self):
        url = '/typeforms/sync/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
