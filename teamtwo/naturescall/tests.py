from django.test import TestCase, Client
from django.urls import reverse
from .models import Restroom
from .views import search
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
        response = self.client.get(reverse('naturescall:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Nature's call")

    def test_missing_restroom(self):
        """
        If the selected restroom is not present in the database,
        the response should be a 404 Error
        """
        response = self.client.get(reverse('naturescall:restroom_detail',
                                           args=(1,)))
        self.assertEqual(response.status_code, 404)

    # def test_invalid_restroom_desc(self):
    #     """
    #     If a restroom's description is under 10 characters,
    #     it should fail to be added to the database
    #     """
    #     desc = "9LTRDESCR"
    #     yelp_id = "E6h-sMLmF86cuituw5zYxw"
    #     rr1 = create_restroom(yelp_id, desc)
    #     response = self.client.get(reverse('naturescall:restroom_detail',
    #                                        args=(1,)))
    #     self.assertEqual(response.status_code, 404)

    def test_one_restroom(self):
        """
        Once a restroom is added, it should be reachable via the
        restroom_detail link
        """
        desc = "TEST DESCRIPTION"
        yelp_id = "E6h-sMLmF86cuituw5zYxw"
        rr1 = create_restroom(yelp_id, desc)
        response = self.client.get(reverse('naturescall:restroom_detail',
                                           args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['res']['desc'], desc)

    def test_restroom_invalid_search(self):
        """
        A search with an invalid search string should yield no results
        but should return a valid webpage
        """
        c = Client()
        response = c.post(reverse('naturescall:search_restroom'),
                          data={'location': "szzzzz"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Location Not Found")

    def test_restroom_valid_search_empty_database(self):
        """
        A search with a valid search string with an empty database
        should return a valid webpage with 20 "Add Restroom" results
        """
        c = Client()
        response = c.post(reverse('naturescall:search_restroom'),
                          data={'location': "nyu tandon"})
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
        rr1 = create_restroom(yelp_id, desc)
        response = c.post(reverse('naturescall:search_restroom'),
                          data={'location': "nyu tandon"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content).count("Add Restroom"), 19)

# class ViewHelperFunctionTests(TestCase):
#
#     def test_bad_yelp_input(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)