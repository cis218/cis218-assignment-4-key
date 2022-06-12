from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
