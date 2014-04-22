from decimal import *

from django.contrib.auth.models import User


from interests.models import Interest, UserInterestAnswer

def points(request_user, matched_user):
	logged_in_user_interests =  UserInterestAnswer.objects.filter(user=request_user)
	viewed_user_interests =  UserInterestAnswer.objects.filter(user=matched_user)
	total_interests = 0
	points_awarded = 0
	points_possible = 0

	for i in logged_in_user_interests:
		for i2 in viewed_user_interests:
			if i.interest == i2.interest:
				total_interests +=1
				points_possible += i.points
				if i.importance_level == i2.importance_level:
					points_awarded += i.points

	try:
		percentage = points_awarded/Decimal(points_possible)
	except: 
		percentage = 0
	print "Out %s interests, %s points were awarded of %s points with a score of %s" %(
		total_interests, points_awarded, points_possible, percentage)
	return total_interests, percentage

def match_percentage(usera, userb):
	a_interests, a_percent = points(usera, userb)
	b_interests, b_percent = points(userb, usera)

	if a_interests == b_interests:
		new_percent = Decimal(a_percent * b_percent)
		n = Decimal(1.0/a_interests)
		match_percent = new_percent ** n
		print match_percent
		return match_percent