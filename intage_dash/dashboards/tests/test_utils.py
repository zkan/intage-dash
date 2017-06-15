from django.test import TestCase

from ..utils import clean_html


class DashboardUtilsTest(TestCase):
    def test_clean_html_should_strip_html_out(self):
        raw_html = '<html><strong>abc</strong><p>test</p></html>'
        result = clean_html(raw_html)
        self.assertEqual(result, 'abctest')
