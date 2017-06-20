from django.core.urlresolvers import reverse
from django.test import TestCase

from form_submissions.models import FormResponse
from typeforms.models import Typeform


class DashboardViewTest(TestCase):
    def setUp(self):
        typeform_uid = 'iSEzWG'
        token = 'e65c13cb2a33255ff8d49994c8971e44'
        answers = {
            'rating_53456466': 3,
            'rating_53701739': 4,
            'rating_53748628': 9,
        }
        payload = {
            'questions': [
                {
                    'id': 'group_53700090',
                    'field_id': 53700090,
                    'question': 'This is just a question group'
                },
                {
                    'id': 'rating_53456466',
                    'group': 'group_53700090',
                    'field_id': 53456466,
                    'question': 'Give me some rate.'
                },
                {
                    'id': 'group_53701933',
                    'field_id': 53701933,
                    'question': 'Another question group'
                },
                {
                    'id': 'rating_53701739',
                    'group': 'group_53701933',
                    'field_id': 53701739,
                    'question': 'Test another rating'
                },
                {
                    'id': 'rating_53748628',
                    'field_id': 53748628,
                    'question': 'Extra question'
                },
            ],
            'responses': [
                {
                    'token': token,
                    'answers': answers,
                },
            ]
        }
        typeform = Typeform.objects.create(
            uid=typeform_uid,
            payload=payload
        )
        FormResponse.objects.create(
            typeform=typeform,
            answers=answers,
            token=token
        )
        self.url = reverse(
            'dashboard',
            kwargs={
                'typeform_uid': typeform_uid
            }
        )

    def test_dashboard_view_should_be_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_should_include_google_chart_api_script(self):
        response = self.client.get(self.url)
        expected = '<script type="text/javascript" ' \
            'src="https://www.gstatic.com/charts/loader.js"></script>'
        self.assertContains(response, expected, status_code=200)

    def test_dashboard_view_should_render_charts(self):
        response = self.client.get(self.url)

        expected = 'google.charts.load("current", ' \
            '{"packages": ["corechart"]});'
        self.assertContains(response, expected, status_code=200)

        expected = 'google.charts.setOnLoadCallback(group_53700090);'
        self.assertContains(response, expected, status_code=200)

        expected = 'function group_53700090()'
        self.assertContains(response, expected, status_code=200)

        expected = '[\'Give me some rate.\', 3.0],'
        self.assertContains(response, expected, status_code=200)

        expected = 'title: "This is just a question group...",'
        self.assertContains(response, expected, status_code=200)

        expected = 'var chart = new google.visualization.ColumnChart' \
            '(document.getElementById(\'group_53700090\'));'
        self.assertContains(response, expected, status_code=200)

        expected = '<div id="group_53700090"></div>'
        self.assertContains(response, expected, status_code=200)

        expected = 'google.charts.setOnLoadCallback(group_53701933);'
        self.assertContains(response, expected, status_code=200)

        expected = 'function group_53701933()'
        self.assertContains(response, expected, status_code=200)

        expected = '[\'Test another rating\', 4.0],'
        self.assertContains(response, expected, status_code=200)

        expected = 'title: "Another question group...",'
        self.assertContains(response, expected, status_code=200)

        expected = 'var chart = new google.visualization.ColumnChart' \
            '(document.getElementById(\'group_53701933\'));'
        self.assertContains(response, expected, status_code=200)

        expected = '<div id="group_53701933"></div>'
        self.assertContains(response, expected, status_code=200)

        expected = 'google.charts.setOnLoadCallback(group_others);'
        self.assertContains(response, expected, status_code=200)

        expected = 'function group_others()'
        self.assertContains(response, expected, status_code=200)

        expected = '[\'Extra question\', 9.0],'
        self.assertContains(response, expected, status_code=200)

        expected = 'title: "Others",'
        self.assertContains(response, expected, status_code=200)

        expected = 'var chart = new google.visualization.ColumnChart' \
            '(document.getElementById(\'group_others\'));'
        self.assertContains(response, expected, status_code=200)

        expected = '<div id="group_others"></div>'
        self.assertContains(response, expected, status_code=200)


class DashboardBranchViewTest(TestCase):
    def setUp(self):
        typeform_uid = 'iSEzWG'
        token = 'e65c13cb2a33255ff8d49994c8971e44'
        another_token = 'a81c13cb2a33255ff8d49994c8971e55'
        answers = {
            'list_53368385_choice': 'BKK',
            'rating_53456466': 3,
            'rating_53701739': 4,
            'rating_53748628': 9,
        }
        another_answers = {
            'list_53368385_choice': 'Phuket',
            'rating_53456466': 5,
            'rating_53701739': 6,
            'rating_53748628': 3,
        }
        payload = {
            'questions': [
                {
                    'field_id': 53368385,
                    'id': 'list_53368385_choice',
                    'question': 'Branch?'
                },
                {
                    'id': 'group_53700090',
                    'field_id': 53700090,
                    'question': 'This is just a question group'
                },
                {
                    'id': 'rating_53456466',
                    'group': 'group_53700090',
                    'field_id': 53456466,
                    'question': 'Give me some rate.'
                },
                {
                    'id': 'group_53701933',
                    'field_id': 53701933,
                    'question': 'Another question group'
                },
                {
                    'id': 'rating_53701739',
                    'group': 'group_53701933',
                    'field_id': 53701739,
                    'question': 'Test another rating'
                },
                {
                    'id': 'rating_53748628',
                    'field_id': 53748628,
                    'question': 'Extra question'
                },
            ],
            'responses': [
                {
                    'token': token,
                    'answers': answers,
                },
            ]
        }
        typeform = Typeform.objects.create(
            uid=typeform_uid,
            payload=payload
        )
        FormResponse.objects.create(
            typeform=typeform,
            answers=answers,
            token=token
        )
        FormResponse.objects.create(
            typeform=typeform,
            answers=another_answers,
            token=another_token
        )
        self.url = reverse(
            'dashboard_branch',
            kwargs={
                'typeform_uid': typeform_uid
            }
        )

    def test_dashboard_branch_view_should_be_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_branch_view_should_include_google_chart_api_script(
        self
    ):
        response = self.client.get(self.url)
        expected = '<script type="text/javascript" ' \
            'src="https://www.gstatic.com/charts/loader.js"></script>'
        self.assertContains(response, expected, status_code=200)

    def test_dashboard_branch_view_should_render_charts_for_each_branch(self):
        response = self.client.get(self.url)

        expected = 'google.charts.load("current", ' \
            '{"packages": ["corechart"]});'
        self.assertContains(response, expected, status_code=200)

        expected = '[\'Score\', \'Phuket (1)\', \'BKK (1)\']'
        self.assertContains(response, expected, count=3, status_code=200)

        expected = 'google.charts.setOnLoadCallback(group_53700090);'
        self.assertContains(response, expected, status_code=200)

        expected = 'function group_53700090()'
        self.assertContains(response, expected, status_code=200)

        expected = '[\'Give me some rate.\', 5.0, 3.0],'
        self.assertContains(response, expected, status_code=200)

        expected = 'title: "This is just a question group...",'
        self.assertContains(response, expected, status_code=200)

        expected = 'var chart = new google.visualization.ColumnChart' \
            '(document.getElementById(\'group_53700090\'));'
        self.assertContains(response, expected, status_code=200)

        expected = '<div id="group_53700090"></div>'
        self.assertContains(response, expected, status_code=200)

        expected = 'google.charts.setOnLoadCallback(group_53701933);'
        self.assertContains(response, expected, status_code=200)

        expected = 'function group_53701933()'
        self.assertContains(response, expected, status_code=200)

        expected = '[\'Test another rating\', 6.0, 4.0],'
        self.assertContains(response, expected, status_code=200)

        expected = 'title: "Another question group...",'
        self.assertContains(response, expected, status_code=200)

        expected = 'var chart = new google.visualization.ColumnChart' \
            '(document.getElementById(\'group_53701933\'));'
        self.assertContains(response, expected, status_code=200)

        expected = '<div id="group_53701933"></div>'
        self.assertContains(response, expected, status_code=200)

        expected = 'google.charts.setOnLoadCallback(group_others);'
        self.assertContains(response, expected, status_code=200)

        expected = 'function group_others()'
        self.assertContains(response, expected, status_code=200)

        expected = '[\'Extra question\', 3.0, 9.0]'
        self.assertContains(response, expected, status_code=200)

        expected = 'title: "Others",'
        self.assertContains(response, expected, status_code=200)

        expected = 'var chart = new google.visualization.ColumnChart' \
            '(document.getElementById(\'group_others\'));'
        self.assertContains(response, expected, status_code=200)

        expected = '<div id="group_others"></div>'
        self.assertContains(response, expected, status_code=200)
