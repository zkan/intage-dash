from django.contrib.auth.models import User
from django.test import TestCase

from ..models import FormResponse
from typeforms.models import Typeform


class FormResponseAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@pronto.com', 'admin')
        self.client.login(username='admin', password='admin')
        self.url = '/admin/form_submissions/formresponse/'

    def test_form_response_admin_should_be_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_response_admin_should_have_columns(self):
        typeform = Typeform.objects.create(
            uid='abc',
            payload=[]
        )
        FormResponse.objects.create(
            typeform=typeform,
            answers=[]
        )
        response = self.client.get(self.url)

        expected = '<div class="text"><a href="?o=1">Typeform</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=2">Answers</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)

        expected = '<div class="text"><a href="?o=3">Token</a></div>'
        self.assertContains(response, expected, count=1, status_code=200)
