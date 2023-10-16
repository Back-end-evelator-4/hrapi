from django.test import TestCase, Client
from django.contrib.auth.models import User
from ..models import Post


class TestPostModel(TestCase):

    # def setUp(self) -> None:
    #     print('working..')
    #     self.testuser1 = User.objects.create_user(
    #         username='testuser1',
    #         password='12345',
    #     )
    #     self.testuser2 = User.objects.create_user(
    #         username='testuser2',
    #         password='12345',
    #     )
    #     self.post = Post.objects.create(
    #         title='test title 1',
    #         content='test content 1'
    #     )


    @classmethod
    def setUpTestData(cls):
        print('working..')
        cls.testuser1 = User.objects.create_user(
            username='testuser1',
            password='12345',
        )
        cls.testuser2 = User.objects.create_user(
            username='testuser2',
            password='12345',
        )
        cls.post = Post.objects.create(
            title='test title 1',
            content='test content 1'
        )

        c = Client()
        cls.user = c.login(username='testuser1', password='12345')

    def setUp(self) -> None:
        self.user2 = self.client.login(username='testuser2', password='12345')

    def test_str(self):
        self.assertEqual(str(self.post), 'test title 1')

    def test_liked_users(self):
        self.post.likes.add(self.testuser1.id)
        self.post.likes.add(self.testuser2.id)

        self.assertEqual(self.post.likes.count(), 2)


    def test_get_absolute_url(self):
        self.post.likes.set([self.testuser1.id, self.testuser2.id])

        expected_path = '/blog/detail/test-title-1/'

        self.assertEqual(self.post.get_absolute_url(), expected_path)
