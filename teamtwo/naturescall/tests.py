from django.test import TestCase
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

    def test_one_restroom(self):
        """
        Once a restroom is added, it should be reachable via the
        restroom_detail link
        """
        desc = "FAKE DESCRIPTION"
        yelp_id = "E6h-sMLmF86cuituw5zYxw"
        rr1 = create_restroom(yelp_id, desc)
        response = self.client.get(reverse('naturescall:restroom_detail',
                                           args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, desc)

    def test_restroom_invalid_search_empty_database(self):
        """
        A search with an invalid search string should yield no results
        but should return a valid webpage
        """
        response = self.client.post(reverse('naturescall:index'),
                                    data={'form':{'location':"szzzzz"}})
        self.assertEqual(response.status_code, 200)
        print(response.__dict__)
        # self.assertContains(response, "Welcome")

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