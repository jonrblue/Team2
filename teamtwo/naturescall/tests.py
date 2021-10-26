from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restroom
import os

api_key = str(os.getenv("yelp_key"))

API_HOST = "https://api.yelp.com"
SEARCH_PATH = "/v3/businesses/search"
BUSINESS_PATH = "/v3/businesses/"


def create_restroom(yelp_id, desc):
    """
    Create a restroom with the given parameters. Other parameters are
    left at their default values
    """
    return Restroom.objects.create(yelp_id=yelp_id, Description=desc)


class ViewTests(TestCase):
    def test_index(self):
        """
        If index is fetched, the response should contain welcome message"
        """
        response = self.client.get(reverse("naturescall:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Nature's call")

    def test_missing_restroom(self):
        """
        If the selected restroom is not present in the database,
        the response should be a 404 Error
        """
        response = self.client.get(reverse("naturescall:restroom_detail", args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_one_restroom_via_create(self):
        """
        Once a restroom is added using create, it should be
        reachable via the restroom_detail link
        """
        desc = "TEST DESCRIPTION"
        yelp_id = "E6h-sMLmF86cuituw5zYxw"
        create_restroom(yelp_id, desc)
        response = self.client.get(reverse("naturescall:restroom_detail", args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["res"]["desc"], desc)

    def test_one_restroom_via_form_not_logged_in(self):
        """
        Trying to add a restroom via the form when not logged in
        should result in a redirect to the login page. That restroom's
        page then should not exist.
        """
        c = Client()
        desc = "TEST DESCRIPTION"
        yelp_id = "E6h-sMLmF86cuituw5zYxw"
        response = c.post(
            reverse("naturescall:add_restroom", args=(1,)),
            data={"yelp_id": yelp_id, "Description": desc},
        )
        response2 = c.get(reverse("naturescall:restroom_detail", args=(1,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 404)

    def test_one_restroom_via_form_logged_in(self):
        """
        A logged in user should be able to add a restroom via the form.
        Once added, the restroom page should be accessible.
        """
        c = Client()
        user = User.objects.create_user("Jon", "jon@email.com")
        c.force_login(user=user)
        desc = "TEST DESCRIPTION"
        yelp_id = "E6h-sMLmF86cuituw5zYxw"
        response = c.post(
            reverse("naturescall:add_restroom", args=(1,)),
            data={"yelp_id": yelp_id, "Description": desc},
        )
        response2 = c.get(reverse("naturescall:restroom_detail", args=(1,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 200)

    def test_one_restroom_invalid_form_logged_in(self):
        """
        A restroom with an invalid description should not be added
        """
        c = Client()
        user = User.objects.create_user("Jon", "jon@email.com")
        c.force_login(user=user)
        desc = "9LTRDESCR"
        yelp_id = "E6h-sMLmF86cuituw5zYxw"
        response = c.post(
            reverse("naturescall:add_restroom", args=(1,)),
            data={"yelp_id": yelp_id, "Description": desc},
        )
        response2 = c.get(reverse("naturescall:restroom_detail", args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 404)

    def test_restroom_invalid_search(self):
        """
        A search with an invalid search string should yield no results
        but should return a valid webpage
        """
        c = Client()
        response = c.post(
            reverse("naturescall:search_restroom"), data={"searched": "szzzzz"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Location Not Found")

    def test_restroom_valid_search_empty_database(self):
        """
        A search with a valid search string with an empty database
        should return a valid webpage with 20 "Add Restroom" results
        """
        c = Client()
        response = c.post(
            reverse("naturescall:search_restroom"), data={"searched": "nyu tandon"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content).count("Add Restroom"), 20)

    def test_restroom_valid_search_one_element_database(self):
        """
        A search with a valid search string with a database with one element
        should return a valid webpage with 19 "Add Restroom" results
        """
        c = Client()
        desc = "TEST DESCRIPTION"
        yelp_id = "E6h-sMLmF86cuituw5zYxw"
        create_restroom(yelp_id, desc)
        response = c.post(
            reverse("naturescall:search_restroom"), data={"searched": "nyu tandon"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content).count("Add Restroom"), 19)

    def test_access_signup(self):
        """
        A get request to the signup page should yield a valid response
        """
        c = Client()
        response = c.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
