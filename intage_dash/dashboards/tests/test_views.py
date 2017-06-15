from django.core.urlresolvers import reverse
from django.test import TestCase


class DashboardViewTest(TestCase):
    def setUp(self):
        self.url = reverse('dashboard')

    def test_dashboard_view_should_be_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_should_include_google_chart_api_script(self):
        response = self.client.get(self.url)
        expected = '<script type="text/javascript" ' \
            'src="https://www.gstatic.com/charts/loader.js"></script>'
        self.assertContains(response, expected, status_code=200)
