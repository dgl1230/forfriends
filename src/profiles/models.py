# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User




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


class Info(models.Model):
	user = models.ForeignKey(User)
	bio = models.CharField(max_length=420, null=True, blank=True)
	birthday = models.DateField(null=True, blank=True)
	first_name = models.CharField(max_length=20, null=True, blank=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
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

	'''def save(self, *args, **kwargs):
		if self.is_profile_pic:
			try:
				temp = UserPicture.objects.filter(user=self.user).get(is_profile_pic=True)
				if self != temp:
					temp.is_profile_pic = False
					temp.save()
			except UserPicture.DoesNotExist:
				pass
			super(UserPicture, self).save(*args, **kwargs)'''