# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User





class Category(models.Model):
	title = models.CharField(max_length=120)

	def __unicode__(self):
		return str(self.title)



class Interest(models.Model):
	category = models.ForeignKey(Category, null=True, blank=True)
	interest = models.CharField(max_length=120)
	approved = models.BooleanField(default=False)

	def __unicode__(self):
		return self.interest



class UserInterestAnswer(models.Model):
	user = models.ForeignKey(User)
	interest = models.ForeignKey(Interest)

	def __unicode__(self):
		return self.interest.interest

