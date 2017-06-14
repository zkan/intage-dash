from django.test import TestCase


class ResponseWebhookViewTest(TestCase):
    def test_webhook_view_should_accept_post_request(self):
        url = '/submissions/webhook/'
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)
