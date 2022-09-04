from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Twit, Comment


class TwitTests(TestCase):
    """Twit Tests"""

    @classmethod
    def setUpTestData(cls):
        """Set Up Test Data"""
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )

        cls.twit = Twit.objects.create(
            body="Nice twit content",
            image_url="https://example.com/example.png",
            user=cls.user,
        )

        cls.comment = Comment.objects.create(
            twit=cls.twit,
            user=cls.user,
            text="Nice comment content",
        )

        cls.other_user = get_user_model().objects.create_user(
            username="otheruser",
            email="other@email.com",
            password="secret",
        )

        cls.other_twit = Twit.objects.create(
            body="Nice other twit content",
            user=cls.user,
        )

        cls.other_comment = Comment.objects.create(
            twit=cls.twit,
            user=cls.other_user,
            text="Nice other comment content",
        )

    def test_twit_model(self):
        """Test Twit Model"""
        self.assertEqual(self.twit.body, "Nice twit content")
        self.assertEqual(self.twit.user.username, "testuser")
        self.assertEqual(str(self.twit), "Nice twit content")
        self.assertEqual(self.twit.get_like_url(), "/twits/1/like/")

    def test_comment_model(self):
        """Test Comment Model"""
        self.assertEqual(self.comment.text, "Nice comment content")
        self.assertEqual(self.comment.user.username, "testuser")
        self.assertEqual(str(self.comment), "Nice comment content")

    def test_url_root_redirects_to_listview(self):
        """Test url exists at correct location listview"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_url_exists_at_correct_location_listview(self):
        """Test url exists at correct location listview"""
        self.client.force_login(self.user)
        response = self.client.get("/twits/")
        self.assertEqual(response.status_code, 200)

    def test_twit_listview(self):
        """Test twit listview"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("twit_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, "Nice twit content")
        self.assertContains(response, "Nice comment content")
        self.assertContains(response, "https://example.com/example.png")

        self.assertContains(response, self.other_user.username)
        self.assertContains(response, "Nice other twit content")
        self.assertContains(response, "Nice other comment content")

        self.assertTemplateUsed(response, "twit_list.html")

    def test_twit_createview(self):
        """Test twit createview"""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("twit_new"),
            {
                "body": "New text",
                "author": self.user.id,
                "image_url": "https://example.com/example2.png",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Twit.objects.first().body, "New text")
        self.assertEqual(
            Twit.objects.first().image_url, "https://example.com/example2.png"
        )

    def test_twit_updateview(self):
        """Test twit updateview"""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("twit_edit", args="1"),
            {
                "body": "Updated text",
                "image_url": "https://example.com/example3.png",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Twit.objects.last().body, "Updated text")
        self.assertEqual(
            Twit.objects.last().image_url, "https://example.com/example3.png"
        )

    def test_twit_deleteview(self):
        """Test twit deleteview"""
        self.client.force_login(self.user)
        self.assertEqual(Twit.objects.count(), 2)
        response = self.client.post(reverse("twit_delete", args="1"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Twit.objects.count(), 1)

    def test_comment_createview(self):
        """Test comment createview"""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("comment_new", args="1"),
            {
                "text": "New comment",
                "author": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.last().text, "New comment")

    def test_established_user_like_shows_up(self):
        """Test established user like shows up"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("twit_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<span class="like_count">0</span>')
        self.assertNotContains(response, '<span class="like_count">1</span>')

        self.other_twit.likes.add(self.user)
        self.other_twit.save()

        response = self.client.get(reverse("twit_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<span class="like_count">1</span>')
        self.assertContains(response, '<span class="like_count">0</span>')

        self.twit.likes.add(self.other_user)
        self.twit.save()

        response = self.client.get(reverse("twit_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<span class="like_count">1</span>')
        self.assertNotContains(response, '<span class="like_count">0</span>')
