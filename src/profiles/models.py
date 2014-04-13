from django.db import models
from django.contrib.auth.models import User




GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female')
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
	bio = models.CharField(max_length=420)
	birthday = models.DateField()
	first_name = models.CharField(max_length=20)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	last_name = models.CharField(max_length =20)

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
	image = models.ImageField(upload_to='profiles/')
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	
	active = models.BooleanField(default=True)


	def __unicode__(self):
		return str(self.image)
