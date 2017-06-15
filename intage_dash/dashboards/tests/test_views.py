from django.core.urlresolvers import reverse
from django.test import TestCase


class DashboardViewTest(TestCase):
    def test_dashboard_view_should_be_accessible(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
