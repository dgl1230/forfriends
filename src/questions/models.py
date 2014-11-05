# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	question = models.CharField(max_length=120)
	weight = models.DecimalField(max_digits=2, decimal_places=2, default=1)

	def __unicode__(self):
		return self.question



class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length=200)

	def __unicode__(self):
		return self.answer


class UserAnswer(models.Model):

	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer = models.ForeignKey(Answer, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.answer.answer

