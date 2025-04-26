import re
import time
from unittest import skip

from django.core import mail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from accounts.models import User

# from accounts.forms import ListUserCreationForm
# from accounts.models import ListUser

from .base import FunctionalTest

USERNAME = "edith@example.com"
PASSWORD = "123"
SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):
    def test_signup(self):
        self.browser.get(self.live_server_url)
        # Edith notices a "Sign up" button in the navbar
        navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        self.assertIn("Sign up", navbar.text)
        # She clicks on it
        self.browser.find_element(By.ID, "id_signup").click()
        # She notices the url has changed
        self.wait_for(
            lambda: self.assertIn("/accounts/signup", self.browser.current_url)
        )
        # Edith also notices that there are some fields: email, password and another password input
        self.wait_for(
            lambda: self.assertIn(
                "Email", self.browser.find_element(By.CSS_SELECTOR, "body").text
            )
        )

        # # She decides to enter her email and a password
        email = self.browser.find_element(By.CSS_SELECTOR, "input[name=email]")
        email.send_keys(USERNAME)
        # time.sleep(5)
        password1 = self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "input[name=password1]")
        )
        password1.send_keys(PASSWORD)
        # time.sleep(5)

        password2 = self.browser.find_element(By.CSS_SELECTOR, "input[name=password2]")

        password2.send_keys(PASSWORD)

        # Then clicks on the "Sign Up" button
        self.browser.find_element(By.ID, "id_signup").click()
        # She is back on the home page and notices it says "Logged in as edith@example.com"
        self.wait_for(
            lambda: self.assertIn(
                "Logged in as " + USERNAME,
                self.browser.find_element(By.CSS_SELECTOR, "body").text,
            )
        )
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_logout"),
        )

    def test_login_using_email_and_password(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        user: User = User.objects.create(email=USERNAME)
        user.set_password("123")
        user.save()

        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, "id_login").click()

        self.wait_for(
            lambda: self.assertIn(
                "Email:",
                self.browser.find_element(By.CSS_SELECTOR, "body").text,
            )
        )

        self.browser.find_element(By.CSS_SELECTOR, "input[name=username]").send_keys(
            USERNAME, Keys.ENTER
        )

        self.browser.find_element(By.CSS_SELECTOR, "input[name=password]").send_keys(
            PASSWORD, Keys.ENTER
        )

        self.wait_for(
            lambda: self.assertIn(
                "Logged in as " + USERNAME,
                self.browser.find_element(By.CSS_SELECTOR, "body").text,
            )
        )
        self.wait_for(
            lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_logout"),
        )
        return
        # # She checks her email and finds a message
        # email = mail.outbox.pop()
        # self.assertIn(USERNAME, email.to)
        # self.assertEqual(email.subject, SUBJECT)

        # # It has a URL link in it
        # self.assertIn("Use this link to log in", email.body)
        # url_search = re.search(r"http://.+/.+$", email.body)
        # if not url_search:
        #     self.fail(f"Could not find url in email body:\n{email.body}")
        # url = url_search.group(0)
        # self.assertIn(self.live_server_url, url)

        # # she clicks it
        # self.browser.get(url)

        # # she is logged in!
        # self.wait_for(
        #     lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_logout"),
        # )
        # navbar = self.browser.find_element(By.CSS_SELECTOR, ".navbar")
        # self.assertIn(USERNAME, navbar.text)
