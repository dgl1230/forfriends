# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User




class Interest(models.Model):
	description = models.CharField(max_length=200)
	interest = models.CharField(max_length=120)
	approved = models.BooleanField(default=False)
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
	STRONGLY_LIKE = 'Strongly Like'
	LIKE = 'Like'
	NEUTRAL = 'Neutral'
	DISLIKE = 'Dislike'
	STRONGLY_DISLIKE = 'Strongly Dislike'
	IMPORTANCE_CHOICES = (
		(STRONGLY_LIKE, 'Strongly Like'),
		(LIKE, 'Like'),
		(NEUTRAL, 'Neutral'),
		(DISLIKE, 'Dislike'),
		(STRONGLY_DISLIKE, 'Strongly Dislike'),
	)
	user = models.ForeignKey(User)
	interest = models.ForeignKey(Interest)
	importance_level = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES,
							default=NEUTRAL, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.interest.interest

class Category(models.Model):
	interests = models.ManyToManyField(Interest)
	title = models.CharField(max_length=120)
	slug = models.SlugField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.title)
