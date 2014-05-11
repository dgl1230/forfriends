from decimal import Decimal


from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in



class MatchList(models.Model):
	user = models.ForeignKey(User, related_name='main_user')
	match = models.ForeignKey(User, related_name='matched_user')
	read = models.BooleanField(default=False)
	read_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.user.username)

	class Meta:
		ordering = ['-updated', '-timestamp']

def login_user_matches(sender, user, request, **kwargs):
		obj = Match.objects.filter(from_user=user)
		for abc in obj:
			if abc.to_user != user:
				#if Match.objects.good_match(abc.to_user, user):
				add_to_list, created = MatchList.objects.get_or_create(user=user, match=abc.to_user)
		obj2 = Match.objects.filter(to_user=user)
		for abc in obj2:
			if abc.from_user != user:
				#if Match.objects.good_match(abc.from_user, user):
				add_to_list, created = MatchList.objects.get_or_create(user=user, match=abc.from_user)
		request.session['new_matches_count'] = MatchList.objects.filter(user=user).filter(read=False).count()

user_logged_in.connect(login_user_matches)



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