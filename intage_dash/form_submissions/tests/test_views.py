import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import FormResponse
from typeforms.models import Typeform


class ResponseWebhookViewTest(TestCase):
    def setUp(self):
        self.typeform = Typeform.objects.create(
            uid='HQnxZM',
            payload={}
        )
        self.data = {
            'form_response': {
                'form_id': 'HQnxZM',
                'token': '2d5a18110c274a2f93958599918df1a7',
                'answers': [
                    {
                        'field': {
                            'type': 'multiple_choice',
                            'id': '53368385'
                        },
                        'type': 'choice',
                        'choice': {
                            'label': 'BKK'
                        }
                    },
                    {
                        'field': {
                            'type': 'rating',
                            'id': '53368586'
                        },
                        'type': 'number',
                        'number': 7
                    }
                ]
            }
        }
        self.url = reverse('submission_webhook')

    def test_webhook_view_should_accept_post_request(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_webhook_view_should_create_response_when_receive_post_request(
        self
    ):
        self.client.post(
            self.url,
            data=json.dumps(self.data),
            content_type='application/json'
        )

        form_responses = FormResponse.objects.filter(typeform=self.typeform)

        self.assertEqual(len(form_responses), 1)

        expected_answers = {
            'list_53368385_choice': 'BKK',
            'rating_53368586': 7
        }
        self.assertDictEqual(form_responses[0].answers, expected_answers)

        expected_token = '2d5a18110c274a2f93958599918df1a7'
        self.assertEqual(form_responses[0].token, expected_token)
