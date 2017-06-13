from django.contrib.auth.models import User
from django.test import TestCase


class TypeformAdminTest(TestCase):
    def test_typeform_admin_should_be_accessible(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')

        url = '/admin/typeforms/typeform/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
