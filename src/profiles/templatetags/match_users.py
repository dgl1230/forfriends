from django.contrib.auth.models import User
from django import template

from matches.models import Match

register = template.Library()

@register.filter(name='match_users')
def match_users(request, username):
	user = User.objects.get(username=username)
	set_match, created = Match.objects.get_or_create(from_user=request.user, to_user=single_user)
	try:
		set_match.percent = round(match_percentage(request.user, single_user), 4)
	except: 
		set_match.percent = 0
	set_match.good_match = Match.objects.good_match(request.user, single_user)
	set_match.save()
	match = set_match.percent * 100
	return match 
