from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tweeter.models import Twit, Comment


class SignupPageTests(TestCase):
    """Signup Page Tests"""

    def test_url_exists_at_correct_location_signupview(self):
        """Test url exists at correct location signupview"""
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        """Test signup view name"""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):
        """Test signup form"""
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "testuser@email.com",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, "testuser")
        self.assertEqual(get_user_model().objects.all()[0].email, "testuser@email.com")


class ProfilePageTests(TestCase):
    """Profile Page Tests"""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )

    def test_url_exists_at_correct_location_profileview(self):
        """Test url exists at correct location profileview"""
        self.client.force_login(self.user)
        response = self.client.get(f"/accounts/profile/{self.user.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_profile_view_name(self):
        """Test profile view name"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/profile.html")

    def test_profile_form(self):
        """Test profile form"""
        self.client.force_login(self.user)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        response = self.client.post(
            reverse("profile", kwargs={"pk": self.user.pk}),
            {
                "username": "testuser",
                "email": "test@email.com",
                "first_name": "testy",
                "last_name": "mctester",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@email.com")
        self.assertEqual(self.user.first_name, "testy")
        self.assertEqual(self.user.last_name, "mctester")


class PublicProfilePageTests(TestCase):
    """Public Profile Page Tests"""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )

        cls.twit = Twit.objects.create(
            body="Nice twit content",
            image_url="https://branding.kvcc.edu/assets/Pantone_639/png/Accent_Mark.png",
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
            user=cls.other_user,
        )

        cls.other_comment = Comment.objects.create(
            twit=cls.twit,
            user=cls.other_user,
            text="Nice other comment content",
        )

    def test_url_exists_at_correct_location_public_profileview(self):
        """Test url exists at correct location public profileview"""
        self.client.force_login(self.user)
        response = self.client.get(f"/accounts/public_profile/{self.user.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_profile_view_name(self):
        """Test profile view name"""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("public_profile", kwargs={"pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "public_profile.html")

    def test_public_profile_contents(self):
        """Test public profile contents"""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("public_profile", kwargs={"pk": self.user.pk})
        )
        self.assertContains(response, "testuser")
        self.assertContains(response, "Nice twit content")
        self.assertContains(response, "Nice comment content")
        self.assertContains(response, "Nice other comment content")

        self.assertNotContains(response, "Nice other twit content")

    def test_other_public_profile_contents(self):
        """Test public profile contents"""
        self.client.force_login(self.other_user)
        response = self.client.get(
            reverse("public_profile", kwargs={"pk": self.other_user.pk})
        )
        self.assertContains(response, "otheruser")
        self.assertContains(response, "Nice other twit content")

        self.assertNotContains(response, "Nice twit content")
        self.assertNotContains(response, "Nice comment content")
        self.assertNotContains(response, "Nice other comment content")
