# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
import datetime as dt
import geopy 
from geopy.geocoders import Nominatim 
import googlemaps

# Create your models here.

class restroom_manager(models.Manager):

	def create_location(self, location_name, address, city, state, zip_code):
		obs = restroom.objects.all()

		geolocator = googlemaps.Client(key = 'AIzaSyB9grMKLXPvpVKlo9Eeze72Hm5YLhc8jAg')
		temp = geolocator.geocode("%s, %s, %s, %s" % (address, city, state, zip_code))[0]
		lat_lon = [temp['geometry']['location']['lat'], temp['geometry']['location']['lng']]
		location = self.create(location_name = location_name, address = address, city = city, state = state, zip_code = zip_code)
		location.lat = lat_lon[0]
		location.lng = lat_lon[1]
		location.restroom_id = len(obs)
		return location

class restroom(models.Model):
	restroom_id = models.CharField(max_length = 50)
	location_name = models.CharField(max_length = 50)
	address = models.CharField(max_length = 50)
	city = models.CharField(max_length = 50)
	state = models.CharField(max_length = 50)
	zip_code = models.CharField(max_length = 50)
	lat = models.FloatField(default = 0)
	lng = models.FloatField(default = 0)
	objects = restroom_manager()

	def __str__(self):
		return self.restroom_id

class review_manager(models.Manager):

	def create_review(self, restroom_id, user_id, review_text, review_num):
		user_id = "Nate"
		date_created = dt.datetime.now()
		review = self.create(review_text = review_text, review_num = review_num)
		review.user_id = user_id
		review.restroom_id = restroom_id
		return review

class review(models.Model):

	review_choices = (
		(0, 0),
		(1, 1),
		(2, 2), 
		(3, 3),
		(4, 4),
		(5, 5),
		(6, 6),
		(7, 7),
		(8, 8),
		(9, 9),
		(10, 10)
	)

	restroom_id = models.CharField(max_length = 50)
	user_id = models.CharField(max_length = 50)
	review_text = models.CharField(max_length = 500)
	review_num = models.PositiveSmallIntegerField(choices = review_choices, default = 0)
	date_created = models.DateField(default = now, blank = True)

	objects = review_manager()

	def __str__(self):
		return self.restroom_id


