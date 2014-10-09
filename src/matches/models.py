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

	currently_in_icebreaker = models.BooleanField(default=False)



	user1_approved = models.BooleanField(default=False)
	user2_approved = models.BooleanField(default=False)
	are_friends = models.BooleanField(default=False)
	
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.user1.username) +'|' + str(self.user2.username)