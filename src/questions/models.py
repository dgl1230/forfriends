# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	question = models.CharField(max_length=120)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)
	for_new_users = models.BooleanField(default=False)
	is_important_question = models.BooleanField(default=False)

	def __unicode__(self):
		return self.question


NUMBER_CHOICES = (
	(1, 1),
	(2, 2),
	(3, 3), 
	(4, 4), 
	(5, 5),
)


class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length=200)
	pattern_number = models.IntegerField(choices=NUMBER_CHOICES, null=True, blank=True, max_length=20)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.answer

class UserAnswer(models.Model):
	VERY_IMPORTANT = 'Very Important'
	SOMEWHAT_IMPORTANT = 'Somewhat Important'
	NOT_IMPORTANT = 'Not Important'
	IMPORTANCE_CHOICES = (
		(VERY_IMPORTANT, 'Very Important'),
		(SOMEWHAT_IMPORTANT, 'Somewhat Important'),
		(NOT_IMPORTANT, 'Not Important'),
	)

	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer = models.ForeignKey(Answer, null=True, blank=True)
	importance_level = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES,
							default=SOMEWHAT_IMPORTANT, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.answer.answer

