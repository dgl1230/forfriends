# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from matches.models import Match 




GENDER_CHOICES = (
	('Male', 'Male'),
	('Female', 'Female')
)

class Address(models.Model):
	user = models.ForeignKey(User)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	zipcode = models.IntegerField(max_length=5)
	
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.city


class Gamification(models.Model):
	user = models.ForeignKey(User, related_name="logged_in_user")
	circle = models.ManyToManyField(Match)
	friends_list = models.ManyToManyField(User, related_name="friends_list")
	circle_reset_started = models.DateTimeField(null=True, blank=True)
	circle_time_until_reset = models.DateTimeField(null=True, blank=True)

	icebreaker_reset_started = models.DateTimeField(null=True, blank=True)
	icebreaker_until_reset = models.DateTimeField(null=True, blank=True)

	speed_friend_reset_started = models.DateTimeField(null=True, blank=True)
	speed_friend_until_reset = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return self.user.username

	



class Info(models.Model):
	user = models.ForeignKey(User)
	bio = models.CharField(max_length=420, null=True, blank=True)
	birthday = models.DateField(null=True, blank=True)
	first_name = models.CharField(max_length=20, null=True, blank=True)
	gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
	last_name = models.CharField(max_length =20, null=True, blank=True)

	def __unicode__(self):
		return self.last_name


class Job(models.Model):
	user = models.ForeignKey(User)
	position = models.CharField(max_length=200)
	employer = models.CharField(max_length=200)

	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.position


class UserPicture(models.Model):
	user = models.ForeignKey(User)
	caption = models.CharField(max_length=100, null=True, blank=True)
	image = models.ImageField(upload_to='profiles/')
	is_profile_pic = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	
	active = models.BooleanField(default=True)


	def __unicode__(self):
		return str(self.image)

	def save(self, *args, **kwargs):
		if self.is_profile_pic:
			try:
				temp = UserPicture.objects.filter(user=self.user).get(is_profile_pic=True)
				for pic in temp:
					if self != pic:
						pic.is_profile_pic = False
						pic.save()
			except:
				pass
		super(UserPicture, self).save(*args, **kwargs)