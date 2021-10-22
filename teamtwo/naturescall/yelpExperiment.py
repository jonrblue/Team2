# need to import requests, visit:
# https://stackoverflow.com/questions/17309288/importerror-no-module-named-requests
import requests
# import argparse
# import json
# import sys
# import urllib

# from urllib.error import HTTPError
from urllib.parse import quote
# from urllib.parse import urlencode

api_key = "CL1ez7IjEGAsK5LINl-ehN8lTuQSaOqP8NncZD0e8JRLcOmmACCc3u87rtD7l1Bw" \
          "pc9uzwQF8Oj2K6lo7f9cHo2P6xhlCFSI6Thph0MaRgRDcM4XA6iww7AX8QROYXYx"

# API constants, you shouldn't have to change these.
API_HOST = "https://api.yelp.com"
SEARCH_PATH = "/v3/businesses/search"
BUSINESS_PATH = "/v3/businesses/"  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = "food"
DEFAULT_LOCATION = "NYU tandon"
SEARCH_LIMIT = 3


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = "{0}{1}".format(host, quote(path.encode("utf8")))
    headers = {
        "Authorization": "Bearer %s" % api_key,
    }

    print(u"Querying {0} ...".format(url))

    response = requests.request("GET", url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        "term": term.replace(" ", "+"),
        "location": location.replace(" ", "+"),
        "limit": SEARCH_LIMIT,
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


json_obj = search(api_key, "food", "NYU tandon")
print(json_obj)
