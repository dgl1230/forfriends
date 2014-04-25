from decimal import Decimal


from django.db import models
from django.contrib.auth.models import User




class MatchManager(models.Manager):
	def are_matched(self, user1, user2):
		if self.filter(from_user=user1, to_user=user2).count() > 0:
			obj = Match.objects.get(from_user=user1, to_user=user2)
			percentage = obj.percent * 100
			return percentage
		if self.filter(from_user=user2, to_user=user1).count() > 0:
			obj = Match.objects.get(from_user=user2, to_user=user1)
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
	to_user = models.ForeignKey(User, related_name="match")
	from_user = models.ForeignKey(User, related_name="match2")
	percent = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0.00'))
	good_match = models.BooleanField(default=False)

	objects = MatchManager()

	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.percent