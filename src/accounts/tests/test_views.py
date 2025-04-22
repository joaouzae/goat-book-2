from unittest import skip
from django.contrib import auth
from django.test import TestCase

from accounts.models import User


USERNAME = "edith@example.com"
PASSWORD = "123"


class SignupViewTest(TestCase):
    def test_renders_signup_template(self):
        response = self.client.get("/accounts/signup")
        self.assertTemplateUsed(response, "signup.html")

    def test_signup_page_shows_up(self):
        response = self.client.get("/accounts/signup")
        self.assertContains(response, "Sign up")
        self.assertContains(response, "Email:")
        self.assertContains(response, "Password:")

    def test_create_user_if_there_is_no_user_with_that_email_then_login(self):
        anon_user = auth.get_user(self.client)
        self.assertEqual(anon_user.is_authenticated, False)

        self.client.post(
            "/accounts/signup",
            data={"email": USERNAME, "password1": PASSWORD, "password2": PASSWORD},
        )

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.email, "edith@example.com")

    def test_signs_up_and_logs_in_existing_user(self):
        edith: User = User.objects.create_user(USERNAME)
        edith.set_password(PASSWORD)
        edith.save()

        anon_user = auth.get_user(self.client)
        self.assertEqual(anon_user.is_authenticated, False)

        self.client.post(
            "/accounts/signup",
            data={
                "email": USERNAME,
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )

        # verifica se a edith tá logada
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.email, "edith@example.com")


class LoginViewTest(TestCase):
    def test_renders_signup_template(self):
        response = self.client.get("/accounts/login")
        self.assertTemplateUsed(response, "login.html")

    def test_signup_page_shows_up(self):
        response = self.client.get("/accounts/login")
        self.assertContains(response, "Log in")
        self.assertContains(response, "Email:")
        self.assertContains(response, "Password:")

    def test_logs_in_if_correct_credentials(self):
        edith: User = User.objects.create_user(USERNAME)
        edith.set_password(PASSWORD)
        edith.save()

        anon_user = auth.get_user(self.client)
        self.assertEqual(anon_user.is_authenticated, False)

        response = self.client.post(
            "/accounts/login", data={"email": USERNAME, "password": PASSWORD}
        )

        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(user.email, "edith@example.com")

    def test_does_NOT_log_in_if_INcorrect_credentials(self):
        edith: User = User.objects.create_user(USERNAME)
        edith.set_password(PASSWORD)
        edith.save()

        anon_user = auth.get_user(self.client)
        self.assertEqual(anon_user.is_authenticated, False)

        response = self.client.post(
            "/accounts/login",
            data={"email": USERNAME, "password": "senha_errada"},
            follow=True,
        )

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Invalid email or password",
        )
        self.assertEqual(message.tags, "error")

        anon_user = auth.get_user(self.client)
        self.assertEqual(anon_user.is_authenticated, False)


# class LogoutViewTest(TestCase):
#     def
