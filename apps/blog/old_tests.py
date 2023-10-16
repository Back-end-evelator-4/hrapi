from django.test import TestCase
from django.urls import reverse


class TestHomePage(TestCase):

    def test_home_page_url(self):
        excepted_val = 200
        url = reverse('blog:homepage')
        client_code = self.client.get(url).status_code
        self.assertEqual(client_code, excepted_val)

