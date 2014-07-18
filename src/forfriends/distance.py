from geopy.geocoders import GoogleV3
from django.contrib.auth.models import User
from profiles.models import Address
from math import radians, cos, sin, asin, sqrt


geolocator = GoogleV3()

#stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	km = 6367 * c
	#convert from km to miles
	miles = km * 0.621371
	return round(miles)


def calc_distance(user1, user2):
	geolocator = GoogleV3()
	user1_address = Address.objects.get(user=user1)
	user2_address = Address.objects.get(user=user2)
	user1_city = user1_address.city
	user2_city = user2_address.city
	user1_state = user1_address.state
	user2_state = user2_address.state
	address1, (latitude1, longitude1) = geolocator.geocode(user1_city + " " + user1_state)
	address2, (latitude2, longitude2) = geolocator.geocode(user2_city + " " + user2_state)
	miles = haversine(longitude1, latitude1, longitude2, latitude2)
	print miles
	return miles	
