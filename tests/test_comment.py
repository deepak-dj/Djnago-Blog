from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from tests.factory import UserFactory, PostFactory, CommentFactory


class TestPostView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.comment = CommentFactory(author=self.user, post=self.post)

    def test_create_comments(self):
        url = reverse("comment-list-create", kwargs={"post_pk": self.post.id})
        payload = {
            "content": "good experience",
            "likes": True
        }
        response = self.client.post(url, data=payload)
        assert response.status_code == 201
        assert response.data.get("author") == {'username': 'xyz', 'email': 'xyz@gmail.com'}
        assert response.data.get("likes") == True
        assert response.data.get("content") == "good experience"

    def test_get_list_comments(self):
        url = reverse("comment-list-create", kwargs={"post_pk": self.post.id})
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data.get("count") == 1
        assert response.data.get("results")[0].get("author") == {'username': 'xyz', 'email': 'xyz@gmail.com'}
        assert response.data.get("results")[0].get("likes") == True
        assert response.data.get("results")[0].get("content") == 'this is a content'

    def test_get_comments(self):
        url = reverse("comment-list-detail", kwargs={"post_pk": self.post.id, "pk": self.comment.id})
        response = self.client.get(url)
        assert response.status_code == 200
        # assert response.data.get("count") == 1
        assert response.data.get("author") == {'username': 'xyz', 'email': 'xyz@gmail.com'}
        assert response.data.get("likes") == True
        assert response.data.get("content") == 'this is a content'

    def test_update_comment(self):
        url = reverse("comment-list-detail", kwargs={"post_pk": self.post.id, "pk": self.comment.id})
        payload = {
            "content": "bad experience",
            "likes": False
        }
        response = self.client.put(url, data=payload)

        assert response.status_code == 200
        assert response.data.get("author") == {'username': 'xyz', 'email': 'xyz@gmail.com'}
        assert response.data.get("likes") == False
        assert response.data.get("content") == "bad experience"

    def test_delete_post(self):
        url = reverse("comment-list-detail", kwargs={"post_pk": self.post.id, "pk": self.comment.id})
        response = self.client.delete(url)

        assert response.status_code == 204
        assert response.data == {'detail': "Comment 'xyz@gmail.com__title' deleted successfully !!!"}
