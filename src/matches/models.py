# -*- coding: utf-8 -*-
from decimal import Decimal


from django.db import models
from django.contrib.auth.models import User




class Match(models.Model):
	user1 = models.ForeignKey(User, related_name="user1")
	user2= models.ForeignKey(User, related_name="user2", null=True, blank=True)
	percent = models.IntegerField(null=True, blank=True)
	distance = models.IntegerField(null=True, blank=True)

	is_same_state = models.BooleanField(default=False)
	#is true if match is between 0 and 10 miles
	is_10_miles = models.BooleanField(default=False)
	#is true if match is between 11 and 20 miles
	is_20_miles = models.BooleanField(default=False)
	#is true if match is between 21 and 30 miles
	is_30_miles = models.BooleanField(default=False)
	#is true if match is between 31 and 40 miles
	is_40_miles = models.BooleanField(default=False)
	#is true if match is between 41 and 50 miles
	is_50_miles = models.BooleanField(default=False)




	user1_approved = models.BooleanField(default=False)
	user2_approved = models.BooleanField(default=False)
	
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.user1.username) +'|' + str(self.user2.username)