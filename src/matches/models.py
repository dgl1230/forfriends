from decimal import Decimal


from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from interests.matching import points, match_percentage


'''def login_user_matches(sender, user, request, **kwargs):
		obj = Match.objects.filter(user=user)
		for abc in obj:
			if abc.user != user:
				#if Match.objects.good_match(abc.to_user, user):
				add_to_list, created = Match.objects.get_or_create(user=user, matched=abc.matched)
				
		obj2 = Match.objects.filter(user=user)
		for abc in obj2:
			if abc.matched != user:
				#if Match.objects.good_match(abc.from_user, user):
				add_to_list, created = Match.objects.get_or_create(user=user, matched=abc.matched)
		request.session['new_matches_count'] = Match.objects.filter(user=user).count()

user_logged_in.connect(login_user_matches)'''


class MatchManager(models.Manager):
	def are_matched(self, user1, user2):
		if self.filter(user=user1, matched=user2).count() > 0:
			obj = Match.objects.get(user=user1, matched=user2)
			percentage = obj.percent * 100
			return percentage
		if self.filter(user=user2, matched=user1).count() > 0:
			obj = Match.objects.get(user=user2, matched=user1)
			percentage = obj.percent * 100
			return percentage
		else:
			return False

	def good_match(self, user1, user2):
		obj = Match.objects.all()
		percentage = []
		for i in obj:
			percentage.append(i.percent)

		avg_percentage = reduce(lambda x, y: x+y, percentage)/len(percentage) * 100

		if self.are_matched(user1, user2)>= 75.00:
			return True
		else: 
			return False



class Match(models.Model):
	user = models.ForeignKey(User, related_name="match")
	matched = models.ForeignKey(User, related_name="match2", null=True, blank=True)
	percent = models.IntegerField(null=True, blank=True)
	good_match = models.BooleanField(default=False)
	approved = models.BooleanField(default=False)
	objects = MatchManager()

	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.user.username)