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
	return miles	

# Method that checks whether what the user entered is valid or not
# Presumably, Country+State are always valid. If the city is invalid,
# it defaults to a general location of the state. So, we check to see
# if it recognizes the city and return true if so, otherwise return false 
def check_valid_location(user1):
	geolocator = GoogleV3()
	try:
		user1_address = Address.objects.get(user=user1)
		user1_city = user1_address.city
		user1_state = user1_address.state
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

#user1_city = "Poop"
#user1_state = "California"
#address1, (latitude1, longitude1) = geolocator.geocode(user1_city)
#address2, (latitude2, longitude2) = geolocator.geocode(user1_city + " " + user1_state)
#print address1
#print address2