from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post


class DetailViewTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser1',
            password='12345'
        )
        self.post = Post.objects.create(
            title='test title 1',
            content='test content 1'
        )

        self.post.likes.add(self.user)

        self.user = self.client.login(
            username='testuser1',
            password='12345'
        )
        self.factory = RequestFactory()

    def test_detail_view(self):
        url = reverse('blog:detail_page', args=[self.post.slug])
        # request = self.factory.get(url)
        # print(dir(request))
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)


class CreateTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser1',
            password='12345'
        )

        self.user = self.client.login(
            username='testuser1',
            password='12345'
        )

    def test_get_post(self):
        url = reverse('blog:create')
        request = self.client.get(url)
        self.assertEqual(request.status_code, 200)

    def test_create_post(self):
        url = reverse('blog:create')
        data = {
            "title": 'test',
            "content": 'test'
        }
        request = self.client.post(path=url, data=data)
        self.assertRedirects(request, reverse('blog:homepage'))
