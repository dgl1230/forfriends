# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from matches.models import Match


class Visitor(models.Model):
	main_user = models.ForeignKey(User, related_name="main_user")
	visitors = models.ManyToManyField(User, related_name="visitors")

	def __unicode__(self):
		return str(self.main_user.username)
