from naturescall.models import Restroom
from django.shortcuts import render
from django.http import HttpResponse
from .forms import LocationForm
import requests
import argparse
import json
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

api_key = 'CL1ez7IjEGAsK5LINl-ehN8lTuQSaOqP8NncZD0e8JRLcOmmACCc3u87rtD7l1Bwpc9uzwQF8Oj2K6lo7f9cHo2P6xhlCFSI6Thph0MaRgRDcM4XA6iww7AX8QROYXYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
DEFAULT_TERM = 'food'
SEARCH_LIMIT = 10


def index(request):
    context = {}
    form = LocationForm(request.POST or None)
    context['form'] = form
    return render(request, "naturescall/index.html", context)


def yelpSearch(request):
    context = {}
    form = LocationForm(request.POST or None)
    location = request.POST['location']
    k = search(api_key, DEFAULT_TERM, location)
    data = []

    if not k.get('error'):
        data = k['businesses']


    print("The returned json obj is: \n {}".format(data))
    print("End of returned json obj \n")

    # loading rating data from our database
    for restroom in data:
        r_id = restroom['id']
        querySet = Restroom.objects.filter(yelp_id=r_id)
        if not querySet:
            restroom['our_rating'] = 'no rating'
            restroom['db_id'] = ''
        else:
            restroom['our_rating'] = querySet.values()[0]['rating']
            restroom['db_id'] = querySet.values()[0]['id']
            print(restroom['db_id'])

    context['form'] = form
    context['location'] = location
    context['data'] = data
    # print(request.POST)
    return render(request, "naturescall/yelpSearch.html", context)


def restroom(request, r_id):
    """Show a single restroom"""
    querySet = Restroom.objects.filter(id=r_id)
    res = {}
    if querySet:
        #res['id'] = querySet.values()[0]['id']
        #res['yelp_id'] = querySet.values()[0]['yelp_id']
        yelp_id = querySet.values()[0]['yelp_id']
        yelp_data = get_business(api_key, yelp_id)
        yelp_data['db_id'] = r_id
        yelp_data['rating'] = querySet.values()[0]['rating']
        res['yelp_data'] = yelp_data

    context = {'res': res}
    return render(request, "naturescall/restroom.html", context)


def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()


def search(api_key, term, location):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)
