from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Typeform


class TypeformAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')
        self.url = '/admin/typeforms/typeform/'

    def test_typeform_admin_should_be_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_typeform_admin_should_have_columns(self):
        Typeform.objects.create(
            uid='abc',
            payload=[]
        )
        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Uid</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=2">Payload</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)
