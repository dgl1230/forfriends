from geopy.geocoders import GoogleV3
from django.contrib.auth.models import User
from profiles.models import Address
from math import radians, cos, sin, asin, sqrt
import logging

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

#Takes an initial latitude, longitude, and specified radius, and returns domain of latitude
def find_latitude_range(lat1, lon1, radius):
	lon1, lat1, lon2 = map(radians, [lon1, lat1, lon1])
	#latitude is changing, not longitude, so dlon = 0
	#dlon = 0
	c = radius / 6367.0 / 0.621363
	a = (sin(c/2.0))**2
	lat2 = (2 * asin(sqrt(a))) + lat1 
	lat2 = lat2 * 57.2957795 #convert back to degrees from radians
	lat1 = lat1 * 57.2957795
	lat_diff = abs(lat2 - lat1)
	logging.debug("Latitude_diff is: " + str(lat_diff))
	return lat_diff #latitude + lat_diff = right_border, latitude - lat_diff = left_border

#Takes an initial latitude, longitude, and specified radius, and returns domain of longitude
def find_longitude_range(lat1, lon1, radius):
	lon1, lat1, lat2 = map(radians, [lon1, lat1, lat1])
	c = radius / 6367.0 / 0.621363
	a = (sin(c/2.0))**2
	lon2 = 2 * asin(sqrt(a / (cos(lat1) * cos(lat2)))) + lon1
	lon2 = lon2 * 57.2957795 #convert back to degrees from radians
	lon1 = lon1 * 57.2957795
	lon_diff = abs(lon2 - lon1)
	logging.debug("Longitude_diff is: " + str(lon_diff))
	return lon_diff
	#dlat = 0
	#a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	#a = cos(lat1) * cos(lat2) * sin(dlon/2)**2
	#a / (cos(lat1) * cos(lat2)) = sin(dlon/2)**2
	#sqrt(a / (cos(lat1) * cos(lat2))) = sin(dlon/2)
	#2 * asin(sqrt(a / (cos(lat1) * cos(lat2)))) = lon2 - lon1
	#2 * asin(sqrt(a / (cos(lat1) * cos(lat2)))) + lon1 = lon2

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
	return miles	

# Method that checks whether what the user entered is valid or not
# Presumably, Country+State are always valid. If the city is invalid,
# it defaults to a general location of the state. So, we check to see
# if it recognizes the city and return true if so, otherwise return false 
def check_valid_location(city, state):
	geolocator = GoogleV3()
	try:
		#user1_address = Address.objects.get(user=user1)
		user1_city = city
		user1_state = state
		#Check to see if city name on its own is valid somewhere in the world.
		#If not, this line should give an error, and we return False
		address1, (latitude1, longitude1) = geolocator.geocode(user1_city)
		#Check to see if city+state is equal to just state. If it is, then the city is not
		#recognized in the state, so it has defaulted to just state. So, we return false.
		address2, (latitude2, longitude2) = geolocator.geocode(user1_city + " " + user1_state)
		address3, (latitude3, longitude3) = geolocator.geocode(user1_state)
		if (address2 == address3):
			return False
		return True
	except:
		return False 		

def find_nearby_users(logged_in_user, preferred_distance, user_list):
	list_of_nearby_users = []
	#Iterate through list_of_all_users: if calc_distance(logged_in_user, user_i) <= preferred_distance, then add to list_of_nearby_users
	for i in range(len(user_list)):
		temp_user = user_list[i]
		try:
			distance = calc_distance(logged_in_user, temp_user)
			if distance <= preferred_distance:
				list_of_nearby_users.append(temp_user)
		except: 
			pass
	return list_of_nearby_users
	
"""
user1_city = "Poop"
user1_state = "California"
address1, (latitude1, longitude1) = geolocator.geocode(user1_city)
address2, (latitude2, longitude2) = geolocator.geocode(user1_city + " " + user1_state)
print address1
print address2
"""