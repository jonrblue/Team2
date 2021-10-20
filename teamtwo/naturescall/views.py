from naturescall.models import Restroom
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LocationForm
from .forms import AddRestroom
import requests
import argparse
import json
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
import os
from django.urls import reverse
api_key = str(os.getenv('yelp_key'))

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

    k = search(api_key, 'food', location, 10)
    f = search(api_key, 'public', location, 5)
    c = search(api_key, 'restroom', location, 5)

    k_data = f_data = c_data = []

    if not k.get('error'):
        k_data = k['businesses']

    if not f.get('error'):
        f_data = f['businesses']

    if not c.get('error'):
        c_data = c['businesses']

    data = k_data + f_data + c_data

    #data deduplicate
    yelpID_set = set()
    no_dup_data = []
    for restroom in data:
        if restroom['id'] in yelpID_set:
            continue
        yelpID_set.add(restroom['id'])
        no_dup_data.append(restroom)

    data = no_dup_data




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
        addr = str(restroom['location']['display_address'])
        restroom['addr'] = addr.translate(str.maketrans('', '', '[]\''))

    context['form'] = form
    context['location'] = location
    context['data'] = data
    # print(request.POST)
    return render(request, "naturescall/yelpSearch.html", context)

def addR(request, r_id):
    if request.method== 'POST':
        f= AddRestroom(request.POST)
        if f.is_valid():
            post= f.save(commit= False)
            post.save()
            return HttpResponseRedirect(reverse('naturescall:index'))
        else:
            return render(request, "naturescall/addR.html", {'form':f})
    else:
        k= get_business(api_key, r_id)
        context={}
        name= k['name']
        form = AddRestroom(initial= {'yelp_id' : r_id})
        context['form']= form
        context['name']= name
        return render(request, "naturescall/addR.html", context)

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
        yelp_data['Accessible'] = querySet.values()[0]['Accessible']
        yelp_data['FamilyFriendly'] = querySet.values()[0]['FamilyFriendly']
        yelp_data['TransactionRequired'] = querySet.values()[0]['TransactionRequired']

        res['yelp_data'] = yelp_data
        addr = str(yelp_data['location']['display_address'])
        res['addr'] = addr.translate(str.maketrans('', '', '[]\''))

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


def search(api_key, term, location, num):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': num,
        'radius': 900
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)
