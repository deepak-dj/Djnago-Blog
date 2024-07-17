from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from tests.factory import UserFactory, PostFactory, CommentFactory


class TestPostView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.post = PostFactory(author=self.user)
        self.post = CommentFactory(author=self.user, post=self.post)

    def test_get_posts_list(self):
        url = reverse("post-list-create")
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data.get("count") == 1
        assert response.data.get("results")[0].get("author") == {'username': 'xyz', 'email': 'xyz@gmail.com'}
        assert response.data.get("results")[0].get("title") == 'title'
        assert response.data.get("results")[0].get("content") == 'this is a content'
        assert response.data.get("results")[0].get("likes_count") == 1

    def test_get_posts(self):
        url = reverse("post-detail", kwargs={"pk": self.post.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data.get("author") == {'username': 'xyz', 'email': 'xyz@gmail.com'}
        assert response.data.get("title") == 'title'
        assert response.data.get("content") == 'this is a content'
        assert response.data.get("likes_count") == 1

    def test_create_posts(self):
        url = reverse("post-list-create")
        payload = {
            "title": "hellow world..!!",
            "content": "welcome to the world"
        }
        response = self.client.post(url, data=payload)

        assert response.status_code == 201
        assert response.data.get("author") == {'username': 'xyz', 'email': 'xyz@gmail.com'}
        assert response.data.get("title") == "hellow world..!!"
        assert response.data.get("content") == "welcome to the world"

    def test_update_posts(self):
        url = reverse("post-detail", kwargs={"pk": self.post.id})
        payload = {
            "title": "hellow India..!!",
            "content": "welcome to the world"
        }
        response = self.client.put(url, data=payload)

        assert response.status_code == 200
        assert response.data.get("author") == {'username': 'xyz', 'email': 'xyz@gmail.com'}
        assert response.data.get("title") == "hellow India..!!"
        assert response.data.get("content") == "welcome to the world"

    def test_delete_posts(self):
        url = reverse("post-detail", kwargs={"pk": self.post.id})
        response = self.client.delete(url)

        assert response.status_code == 204
        assert response.data == {'detail': "Post 'title' deleted successfully !!!"}