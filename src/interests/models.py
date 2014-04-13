from django.db import models
from django.contrib.auth.models import User


class Interest(models.Model):
	user = models.ForeignKey(User)
	description = models.CharField(max_length=200)
	interest = models.CharField(max_length=120)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.interest

class InterestPicture(models.Model):
	interest = models.ForeignKey(Interest)
	image = models.ImageField(upload_to='profiles/')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return str(self.image)


class UserInterestAnswer(models.Model):
	user = models.ForeignKey(User)
	interest = models.ForeignKey(Interest)
	importance_level = models.CharField(max_length=120, default='Neutral', null=True, blank=True)
	points = models.IntegerField(default='20')
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.interest.interest
