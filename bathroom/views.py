from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.template import loader, Context, RequestContext
from django.template.context import RequestContext

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

import geopy 
import numpy as np
import pandas as pd

from datetime import datetime

from geopy.geocoders import Nominatim #Used to change text to lat and long.

from django.contrib.gis.geoip2 import *
from .models import restroom



#from django.contrib.gis.geoip import GeoIP #Used to get location from IP address


# Create your views here.

def index(request):
	html = loader.get_template('bathroom/index.html')
	return HttpResponse(html.render({}, request))

def login_view(request):
    if request.method == 'POST':
        username = request.POST('username')
        password = request.POST('password')

        user = authenticate(user = username, password = password)

        if user:
            login(request, user)
            t = 'bathroom/maps.html'
            c = {}
            return render(request, t, c)
        else: 
            t = 'registration/login.html'
            c = {}
            return render(request, t, c)

def logout_view(request):
    logout(request)

    return redirect('map')



def signup(request):
    from django.contrib.auth.models import User

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email_add')
        instance = User.objects.create_user(username = username, email = email, password = password)
        instance.first_name = first_name
        instance.last_name = last_name
        instance.save()
        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect('map')

    t = 'registration/signup.html'
    c = {}
    return render(request, t, c)

def map(request):
    from .models import restroom, review
    from django.db.models import Avg
    import googlemaps
    gmaps = googlemaps.Client(key = 'AIzaSyB9grMKLXPvpVKlo9Eeze72Hm5YLhc8jAg')

    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        gmaps = googlemaps.Client(key = 'AIzaSyB9grMKLXPvpVKlo9Eeze72Hm5YLhc8jAg')
        location = gmaps.geocode(str(search_query))[0]
        latitude = location['geometry']['location']['lat']
        longitude = location['geometry']['location']['lng']

    restroom_list = restroom.objects.all()
    restroom_ids = [i.restroom_id for i in restroom_list]
    lat_long_list = [[i.lat, i.lng] for i in restroom_list]
    lat_long_tuple = [(i.lat, i.lng) for i in restroom_list]

    distances = gmaps.distance_matrix(origins = (latitude, longitude),\
    destinations = lat_long_tuple, mode = "walking", units = "imperial")

    if distances['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
        x = range(0, len(restroom_list))
        y = ["NA"] * len(restroom_list)
    else:
        temp = distances['rows'][0]['elements']
        x = []
        y = []
        for i in temp:
            x.append(i['distance']['value'])
            y.append(i['distance']['text'])

    score = []

    for i in restroom_ids:
        temp = review.objects.filter(restroom_id=i).aggregate(Avg('review_num'))
        score.append(round(temp['review_num__avg'], 1))
        
    combo = [{"restroom_id" : i.restroom_id, "location_name" : i.location_name,\
    "address" : i.address, "city" : i.city, "state" : i.state,\
    "zip_code" : i.zip_code, "dist" : j, "dist_text" : k, "score" : l} for i, j, k, l in zip(restroom_list, x, y, score)]

    combo = sorted(combo, key=lambda k: k['dist'], reverse = False) 
    for i in range(1, len(combo)+1):
        combo[i-1]["place_id"] = i

    t = loader.get_template('bathroom/maps.html')

    c = {"latitude" : latitude,
        "longitude" : longitude, 
        "lat_long_list" : lat_long_list,
        "restroom_list" : restroom_list, 
        "distances" : distances,
        "combo" : combo
        }

    return HttpResponse(t.render(c))

@login_required

def add_location(request):

    from .models import restroom
    restroom_list = restroom.objects.all()

    if request.method == "POST":
        instance = restroom()
        location_name = request.POST.get('location_name', None)
        address = request.POST.get('location_address', None)
        city = request.POST.get('location_city', None)
        state = request.POST.get('location_state', None)
        zip_code = request.POST.get('location_zip', None)
        instance = restroom.objects.create_location(location_name, address, city, state, zip_code)
        instance.save()
        return redirect('map')

    t = 'bathroom/add_location.html'
    c = {}
    return render(request, t, c)

@login_required

def add_review(request, restroom_id):
    from .models import review
    review_list = review.objects.all()

    nums = range(0, 11)

    if request.method == "POST":
        instance = review()
        user_id =  "Nate"
        review_text = request.POST.get('review_text', None)
        review_num = request.POST.get('review_num', None)
        instance = review.objects.create_review(restroom_id, user_id, review_text, review_num)
        instance.save()
        return redirect('map')

    t = 'bathroom/add_review.html'
    c = {}
    return render(request, t, c)

