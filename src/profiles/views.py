# -*- coding: utf-8 -*-
import operator 
import datetime
from datetime import date, datetime, timedelta
from random import randint

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.db.models import Q, Max
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.template.loader import get_template
from django.template import Context


from forfriends.settings.deployment import EMAIL_HOST_USER, DEBUG, MEDIA_URL
from forfriends.matching import match_percentage
from forfriends.distance import calc_distance
from matches.models import Match
from .models import Address, Job, Info, UserPicture, Gamification
from .forms import AddressForm, InfoForm, JobForm, UserPictureForm
from interests.models import UserInterestAnswer, Interest
from directmessages.models import DirectMessage
from questions.models import Question, UserAnswer


'''Implements the 'add friend' button when viewing a user's profile
If both users click this button on each other's profile, they can message'''
def add_friend(request, username):
	try: 
		match = Match.objects.get(user1=request.user, user2__username=username)
		match.user1_approved = True
	except: 
		match, created = Match.objects.get_or_create(user1__username=username, user2=request.user)
		match.user2_approved = True

	if (match.user1 == request.user and match.user1_approved == True and match.user2_approved == False):
		requester = request.user
		requested= match.user2
		subject = "Someone wants to be your friend!"
		body = "Hey %s, I think we could be pretty good friends! Why don't you check out my profile and see if you think we'd get along?" %(requested)
		message = DirectMessage.objects.create(subject=subject, body=body, sender=requester, receiver=requested)
		match.save()
		message.save()
		messages.success(request, "%s has received your request!") %(requested)

	if (match.user2 == request.user and match.user2_approved == True and match.user1_approved == False):
		requester = request.user
		requested= match.user1
		subject = "Someone wants to be your friend!"
		body = "Hey %s, I think we could be pretty good friends! Why don't you check out my profile and see if you think we'd get along?" %(requested)
		message = DirectMessage.objects.create(subject=subject, body=body, sender=requester,receiver=requested)
		match.save()
		message.save()
		messages.success(request, "%s has received your request!") %(requested)

	if (match.user1_approved == True and match.user2_approved == True):
		user1 = match.user1
		user2 = match.user2
		match.are_friends = True
		subject = "You have a new friend!"
		body_for_user1 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user2.username)
		body_for_user2 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user1.username)
		user1_message = DirectMessage.objects.create(subject=subject, body=body_for_user1, receiver=user1)
		user2_message = DirectMessage.objects.create(subject=subject, body=body_for_user2, receiver=user2)
		user1_message.sent = datetime.datetime.now()
		user2_message.sent = datetime.datetime.now()
		match.save()
		user1_message.save()
		user2_message.save()
		messages.success(request, "%s also is interested in being your friend - You can now message each other!" %username)
	else:
		messages.success(request, "%s has received your request. If %s is interested too, they will add you!" %(username, username))
	single_user = User.objects.get(username=username)
	match.save()
	if not DEBUG:
		return HttpResponseRedirect('http://www.frenvu.com/discover/?page=%s' % page)
	else: 
		return HttpResponseRedirect('http://127.0.0.1:8000/discover/?page=%s' % page)
	
	return render_to_response('profiles/single_user.html', locals(), context_instance=RequestContext(request))


def add_friend_discovery(request, username, page):
	try: 
		match = Match.objects.get(user1=request.user, user2__username=username)
		match.user1_approved = True
	except: 
		match, created = Match.objects.get_or_create(user1__username=username, user2=request.user)
		match.user2_approved = True

	if (match.user1 == request.user and match.user1_approved == True and match.user2_approved == False):
		requester = request.user
		requested= match.user2
		subject = "Someone wants to be your friend!"
		body = "Hey %s, I think we could be pretty good friends! Why don't you check out my profile and see if you think we'd get along?" %(requested)
		message = DirectMessage.objects.create(subject=subject, body=body, sender=requester, receiver=requested)
		match.save()
		message.save()


	if (match.user2 == request.user and match.user2_approved == True and match.user1_approved == False):
		requester = request.user
		requested= match.user1
		subject = "Someone wants to be your friend!"
		body = "Hey %s, I think we could be pretty good friends! Why don't you check out my profile and see if you think we'd get along?" %(requested)
		message = DirectMessage.objects.create(subject=subject, body=body, sender=requester,receiver=requested)
		match.save()
		message.save()



	if (match.user1_approved == True and match.user2_approved == True):
		user1 = match.user1
		user2 = match.user2
		match.are_friends = True
		subject = "You have a new friend!"
		body_for_user1 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user2.username)
		body_for_user2 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user1.username)
		user1_message = DirectMessage.objects.create(subject=subject, body=body_for_user1, receiver=user1)
		user2_message = DirectMessage.objects.create(subject=subject, body=body_for_user2, receiver=user2)
		user1_message.sent = datetime.datetime.now()
		user2_message.sent = datetime.datetime.now()
		match.save()
		user1_message.save()
		user2_message.save()
		
	
	single_user = User.objects.get(username=username)
	match.save()
	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
	direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
	request.session['num_of_messages'] = direct_messages
	if not DEBUG:
		return HttpResponseRedirect('http://www.frenvu.com/discover/?page=%s' % page)
	else: 
		return HttpResponseRedirect('http://127.0.0.1:8000/discover/?page=%s' % page)


'''
The view for the home page of a user. If they're logged in and not a new user, 
it shows their crowd. If they're logged in and a new user, it redirects them to handle_new_user, 
which will have the user fill in relevant info before they can access the site. Otherwise, 
the user is not logged in, and is shown the landing page.
'''
def all(request):
	if request.user.is_authenticated():
		try: 
			# if both of these statements pass without error, then the user is not new
			info = Info.objects.get(user=request.user)
			assert(info.is_new_user == False)
		except: 
			return HttpResponseRedirect(reverse('handle_new_user'))
		try: 
			# this is to test if somehow the user has multiple circles and fix said error
			user_gamification = Gamification.objects.filter(user=request.user)
			number_of_circles = user_gamification.count()
			# this is to check to make sure the user has users in their circle 
			if number_of_circles == 1:
				user_gamification = Gamification.objects.get(user=request.user)
				i = 0
				for user in user_gamification.circle.all():
					i = i + 1
				#if the user has less than 5 users in their circle, we reset their circle
				if i < 5:
					generate_circle(request.user)
			# if the user has multiple circles, we delete all of their circles
			if number_of_circles > 1:
				user_gamification.delete()
		except:
			pass

		# this is to see if the user has a circle
		try: 
			user_gamification = Gamification.objects.get(user=request.user)
		except: 
			#user does not have a circle
			user_gamification = Gamification.objects.create(user=request.user)
			user_gamification.circle_time_until_reset = datetime.now()
			user_gamification.icebreaker_until_reset = datetime.now()
			user_gamification.save()
			generate_circle(request.user)
		try:
			# check and see if the user has any value in their circle fields
			until_next_reset = user_gamification.circle_time_until_reset.replace(tzinfo=None)
			until_next_icebreaker = user_gamification.icebreaker_until_reset.replace(tzinfo=None)
		except:
			# if they don't, we assign them the current time
			user_gamification.circle_time_until_reset = datetime.now()
			user_gamification.icebreaker_until_reset = datetime.now()
		current_time = datetime.now() 
		until_next_reset = user_gamification.circle_time_until_reset.replace(tzinfo=None)
		hours_until_reset = int((until_next_reset - current_time).total_seconds() / 60 / 60)
		if hours_until_reset <= 1: 
			can_they_reset = True
		else: 
			can_they_reset = False

		until_next_icebreaker = user_gamification.icebreaker_until_reset.replace(tzinfo=None)
		icebreaker_hours_until_reset = int((until_next_icebreaker - current_time).total_seconds() / 60 / 60)
		if icebreaker_hours_until_reset <= 0:
			can_reset_icebreaker = True
		else:
			can_reset_icebreaker = False
		messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
		direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
		request.session['num_of_messages'] = direct_messages
		return render_to_response('all.html', locals(), context_instance=RequestContext(request))



		'''
		try:
			user_gamification = Gamification.objects.get(user=request.user)
			try:
				until_next_reset = user_gamification.circle_time_until_reset.replace(tzinfo=None)
				until_next_icebreaker = user_gamification.icebreaker_until_reset.replace(tzinfo=None)
			except:
				user_gamification.circle_time_until_reset = datetime.now()
				user_gamification.icebreaker_until_reset = datetime.now()
				print 8
			circle = user_gamification.circle.all()
			#since_last_reset = user_gamification.circle_reset_started
			current_time = datetime.now() 
			until_next_reset = user_gamification.circle_time_until_reset.replace(tzinfo=None)
			hours_until_reset = int((until_next_reset - current_time).total_seconds() / 60 / 60)
			if hours_until_reset <= 1: 
				can_they_reset = True
			else: 
				can_they_reset = False

			#since_last_icebreaker = user_gamification.icebreaker_reset_started
			until_next_icebreaker = user_gamification.icebreaker_until_reset.replace(tzinfo=None)
			icebreaker_hours_until_reset = int((until_next_icebreaker - current_time).total_seconds() / 60 / 60)
			if icebreaker_hours_until_reset <= 0:
				can_reset_icebreaker = True
			else:
				can_reset_icebreaker = False
			return render_to_response('all.html', locals(), context_instance=RequestContext(request))
		except: 
			#the user has never calcuated their circle
			try: 
				user_gamification = Gamification.objects.get(user=request.user)

			except: 
				user_gamification = Gamification.objects.create(user=request.user)
				user_gamification.circle_time_until_reset = datetime.now()
				user_gamification.icebreaker_until_reset = datetime.now()
				user_gamification.save()
			generate_circle(request.user)
			try:
				until_next_reset = user_gamification.circle_time_until_reset.replace(tzinfo=None)
				until_next_icebreaker = user_gamification.icebreaker_until_reset.replace(tzinfo=None)
			except:
				user_gamification.circle_time_until_reset = datetime.now()
				user_gamification.icebreaker_until_reset = datetime.now()
			#makes it so that the circle is displayed right away instead of having to click "generate circle"
			user_gamification= Gamification.objects.get(user=request.user)
			#since_last_reset = user_gamification.circle_reset_started
			current_time = datetime.now() 
			until_next_reset = user_gamification.circle_time_until_reset.replace(tzinfo=None)
			hours_until_reset = int((until_next_reset - current_time).total_seconds() / 60 / 60)
			if hours_until_reset <= 1: 
				can_they_reset = True
			else: 
				can_they_reset = False

			#since_last_icebreaker = user_gamification.icebreaker_reset_started
			until_next_icebreaker = user_gamification.icebreaker_until_reset.replace(tzinfo=None)
			icebreaker_hours_until_reset = int((until_next_icebreaker - current_time).total_seconds() / 60 / 60)
			if icebreaker_hours_until_reset <= 0:
				can_reset_icebreaker = True
			else:
				can_reset_icebreaker = False
			return render_to_response('all.html', locals(), context_instance=RequestContext(request))
		'''
			
	else:
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))


'''
def generate_circle(logged_in_user):
	if logged_in_user.is_authenticated(): 
		try: 
			# if this is true, then there are a considerable amount of users who live nearby, so we won't
			# need to create a lot of matches 
			assert (circle_distance(logged_in_user) == 1)
			return
		except: 
			#these variables are for keeping track of users that live within certain miles, ie num_10m is 
			# for users that live within 10 miles
			num_10m = 0
			num_20m = 0
			num_30m = 0
			num_40m = 0
			num_50m = 0 
			users = User.objects.filter(is_active=True).exclude(username=logged_in_user.username).order_by('?')
			for user in users: 
				# if there are some new matches where the users live nearby, we'll break the loop
				if num_10m >= 10 or num_20m >= 10:
					break 
				if user != logged_in_user:
					try: 
						match = Match.objects.get(user1=logged_in_user, user2=user)
					except: 
						match, created = Match.objects.get_or_create(user1=user, user2=logged_in_user)
					try:
						match.distance = round(calc_distance(logged_in_user, user))
						if match.distance <= 10:
							match.percent = match_percentage(match.user1, match.user2)
							num_10m += 1
							num_20m += 1
							num_30m += 1
							num_40m += 1
							num_50m += 1
							# for querying purposes, assigned all fields as true for a user within 10 miles
							# makes things less convoluted
							match.is_10_miles = True
							match.is_20_miles = True 
							match.is_30_miles = True
							match.is_40_miles = True
							match.is_50_miles = True
						elif match.distance <=20:
							num_20m += 1
							num_30m += 1
							num_40m += 1
							num_50m += 1
							match.is_20_miles = True
							match.is_30_miles = True
							match.is_40_miles = True
							match.is_50_miles = True
						elif match.distance <=30:
							num_30m += 1
							num_40m += 1
							num_50m += 1
							match.is_30_miles = True
							match.is_40_miles = True
							match.is_50_miles = True
						elif match.distance <=40:
							num_40m += 1
							num_50m += 1
							match.is_40_miles = True
							match.is_50_miles = True
						elif match.distance <=50: 
							num_50m += 1
							match.is_50_miles = True
						match.save()
					except:
						match.distance = 10000000
			if circle_distance(logged_in_user) == 1:
				return 
			else: 
				# otherwise, there are not very many users who live close by, so we default to 
				# ordering current matches by their percent
				matches = Match.objects.filter(
					Q(user1=logged_in_user) | Q(user2=logged_in_user)
				).exclude(user1=logged_in_user, user2=logged_in_user).order_by('-percent')[:6]
				user_gamification = Gamification.objects.get(user=logged_in_user)
				# so we dont have more than 6-7 users in a circle at a time
				user_gamification.circle.clear()
				for match in matches: 
					user_gamification.circle.add(match) 
				user_gamification.circle_reset_started = datetime.now()
				user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
				user_gamification.save()
'''


def generate_circle(request):
	preferred_distance = 10
	#these variables are for keeping track of users that live within certain miles, ie num_10m is 
	# for users that live within 10 miles
	users = User.objects.filter(is_active=True).exclude(username=request.user.username)
	for user in users: 
		if user != request.user:
			try: 
				match = Match.objects.get(user1=request.user, user2=user)
			except: 
				match, created = Match.objects.get_or_create(user1=user, user2=request.user)
			try:
				match.distance = round(calc_distance(logged_in_user, user))
			except:
				match.distance = 10000000
			match.save()
	if circle_distance(request.user, preferred_distance) == 1:
		pass
	elif circle_distance(request.user, unicode(int(preferred_distance) + 10)) == 1:
		pass
	elif circle_distance(request.user, unicode(int(preferred_distance) + 20)) == 1:
		pass
	elif circle_distance(request.user, unicode(int(preferred_distance) + 30)) == 1:
		pass
	else: 
		# otherwise, there are not very many users who live close by, so we default to 
		# adding to their circle randomly
		user_gamification = Gamification.objects.get(user=request.user)
		current_circle = list(user_gamification.circle.all())
		matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).exclude(user1=request.user, user2=request.user).exclude(are_friends=True).exclude(id__in=[o.id for o in current_circle]).filter(percent__gte=70)
		user_gamification = Gamification.objects.get(user=request.user)
		count = matches.count()
		try:
			max_match = matches.latest('id').id
		except: 
			matches = Match.objects.filter(
				Q(user1=request.user) | Q(user2=request.user)
				).exclude(user1=request.user, user2=request.user).exclude(are_friends=True).exclude(id__in=[o.id for o in current_circle])
		if count < 6:
			matches = Match.objects.filter(
				Q(user1=request.user) | Q(user2=request.user)
				).exclude(user1=request.user, user2=request.user).exclude(are_friends=True).exclude(id__in=[o.id for o in current_circle])
			max_match = matches.latest('id').id
		# so we dont have more than 6-7 users in a circle at a time
		'''
		current_matches = []
		for match in user_gamification.circle.all():
			current_matches.append(match)
		'''
		#current_matches = list(user_gamification.circle.all())
		user_gamification.circle.clear()
		j = 0
		already_chosen = []
		while j < 6:
			try:
				random_index = randint(0, max_match - 1)
				if random_index not in already_chosen:
					random_match = matches[random_index]
					user_gamification.circle.add(random_match)
					already_chosen.append(random_index)
					j += 1
			except:
				pass

		user_gamification.circle_time_until_reset = datetime.now() 
		user_gamification.save()
		#messages.success(request, "We're sorry, but there aren't many users nearby you right now. We rested your circle as best we could, but you can reset it again if you'd like.")

	return HttpResponseRedirect(reverse('home'))




def circle_distance(logged_in_user, preferred_distance):
	user_gamification = Gamification.objects.get(user=logged_in_user)
	current_circle = list(user_gamification.circle.all())
	matches = Match.objects.filter(
		Q(user1=logged_in_user) | Q(user2=logged_in_user)
		).exclude(user1=logged_in_user, user2=logged_in_user).exclude(are_friends=True).filter(percent__gte=70).exclude(id__in=[o.id for o in current_circle]).filter(distance__lte=preferred_distance)
	count = matches.count()
	if matches.count() < 7:
		return 0
	i = 0
	already_chosen = []
	user_gamification.clear()
	max_match = matches.latest('id').id
	while i < 6:
		try:
			random_index = randint(0, max_match - 1)
			if random_index not in already_chosen:
				random_match = matches[random_index]
				user_gamification.circle.add(random_match)
				already_chosen.append(random_index)
				i += 1
		except:
			pass
	user_gamification.circle_reset_started = datetime.now()
	user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
	user_gamification.save()
	return 1




'''
def calculate_circle(request):
	user_gamification = Gamification.objects.get(user=request.user)
	# see if they have any value in the fields of their circle
	try:
		until_next_reset = user_gamification.circle_time_until_reset.replace(tzinfo=None)
		until_next_icebreaker = user_gamification.icebreaker_until_reset.replace(tzinfo=None)
	except:
		# else we assign these values the current time
		user_gamification.circle_time_until_reset = datetime.now()
		user_gamification.icebreaker_until_reset = datetime.now()
	
	current_time = datetime.now() 
	until_next_reset = user_gamification.circle_time_until_reset.replace(tzinfo=None)
	hours_until_reset = int((until_next_reset - current_time).total_seconds() / 60 / 60)
	if hours_until_reset <= 1: 
		generate_circle(request.user)
	else: 
		messages.success(request, "sorry, you need to wait!")
	return HttpResponseRedirect(reverse('home'))
'''


'''
def circle_distance(logged_in_user):
	matches_basic = Match.objects.filter(
			Q(user1=logged_in_user) | Q(user2=logged_in_user)
			).exclude(user1=logged_in_user, user2=logged_in_user)
	matches_10m = matches_basic.filter(is_10_miles=True)
	# if there are 10 users that live within ten miles, we calcualte their circle and break
	# same for users with varying distances
	if matches_10m.count() >= 10: 
		matches = matches_10m.order_by('-percent')[:6]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		user_gamification.circle.clear()
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	matches_20m = matches_basic.filter(is_20_miles=True)
	if matches_20m.count() >= 10:
		matches = matches_20m.order_by('-percent')[:6]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		user_gamification.circle.clear()
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	matches_30m = matches_basic.filter(is_30_miles=True)
	if matches_30m.count() >= 10:
		matches = matches_30m.order_by('-percent')[:6]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		user_gamification.circle.clear()
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	matches_40m = matches_basic.filter(is_40_miles=True)
	if matches_40m.count() >= 10:
		matches = matches_40m.order_by('-percent')[:6]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		user_gamification.circle.clear()
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	matches_50m = matches_basic.filter(is_50_miles=True)
	if matches_50m.count() >= 10:
		matches = match_50m.order_by('-percent')[:6]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		user_gamification.circle.clear()
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	else:
		return 0 
'''



def handle_new_user(request):
	try:
		info = Info.objects.get(user=request.user)
		user_interests = UserInterestAnswer.objects.filter(user=request.user)
		user_questions = UserAnswer.objects.filter(user=request.user)
	except: 
		user_interests = 0
		user_questions = 0
	try: 
		#if we get an error, then this means they signed up with google or facebook
		# so we need to get more info from them first 
		address = Address.objects.get(user=request.user)
		info = Info.objects.get(user=request.user)
		assert(info.signed_up_with_fb_or_goog == False)
	except: 
		return HttpResponseRedirect(reverse('new_user_info'))
	if user_interests.count() < 5:
		return HttpResponseRedirect(reverse('new_user_interests'))
	if user_questions.count() < 10: 
		return HttpResponseRedirect(reverse('new_user_questions'))
	else: 
		info = Info.objects.get(user=request.user)
		info.is_new_user = False
		info.save()
		user_gamification = Gamification.objects.create(user=request.user)

		users = User.objects.filter(is_active=True).exclude(username=request.user.username)
		i = 0
		for user in users: 
			if i > 7:
				break
			if user != request.user:
				try: 
					match = Match.objects.get(user1=request.user, user2=user)
				except: 
					match, created = Match.objects.get_or_create(user1=user, user2=request.user)
				try:
					match.distance = round(calc_distance(logged_in_user, user))
				except:
					match.distance = 10000000
				if match.distance <= 20:
					match.percent = match_percentage(request.user, single_user)
					if match.percent >= 70:
						i += 1

				match.save()

		matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).exclude(user1=request.user, user2=request.user).exclude(are_friends=True).filter(percent__gte=70)
		num_matches = matches.count()
		if num_matches >= 7:
			for match in matches:
				user_gamification.circle.add(match)
		else:
			matches = Match.objects.filter(
				Q(user1=request.user) | Q(user2=request.user)
				).exclude(user1=request.user, user2=request.user).exclude(are_friends=True)
			for match in matches:
				user_gamification.circle.add(match)
		
		user_gamification.circle_time_until_reset = datetime.now()
		user_gamification.icebreaker_until_reset = datetime.now()
		user_gamification.save()
		return HttpResponseRedirect(reverse('home'))
	

#This is the first/second part of registration for users signing up with FB or GOOGerror(request, "Please double check your username or email address and password")
def new_user_info(request):
	if request.POST:
		name = request.POST['name']
		full_name = name.split()
		first_name1 = str(full_name[0])
		first_name2 = first_name1.translate(None, " '?.!/;:@#$%^&(),[]{}`~-_=+*|<>1234567890")
		first_name = first_name2.translate(None, '"')

		if len(first_name) == 0:
			messages.error(request, "Please use only letters first name")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))

		if len(full_name) == 2:
			last_name1 = str(full_name[1])
			last_name2 = last_name1.translate(None, "?.!/;:@#$%^&()`,[]{}~_=+*|<>1234567890")
			last_name = last_name2.translate(None, '"')
			if len(last_name) == 0:
				messages.error(request, "Please use only letters in your last name")
				return render_to_response('home.html', locals(), context_instance=RequestContext(request))

		if len(full_name) >= 3:
			not_first_name = full_name[2:len(full_name)]
			last_name0 = full_name[1]
			for name in not_first_name:
				last_name0 = last_name + " " + name
			last_name1 = str(last_name0)
			last_name2 = last_name1.translate(None, "?.!/;:@#$%^&()`,[]{}~_=+*|<>1234567890")
			last_name = last_name2.translate(None, '"')
			if len(last_name) == 0:
				messages.error(request, "Please use only letters in your last name")
				return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		username1 = str(request.POST['username'])

		username2 = username1.translate(None, " '?.!/;:@#$%^&(),[]{}`~-=+*|<>")
		username = username2.translate(None, '"')

		bad_words = ['shit', 'cunt', 'fuck', 'nigger', 'kyke', 'dyke', 'fag', 'ass', 'rape', 
			'murder', 'kill', 'gook', 'pussy', 'bitch', 'damn', 'hell', 'whore', 'slut', 
			'cum', 'jizz', 'clit', 'anal', 'cock', 'molest', 'necro', 'satan', 'devil', 
			'pedo', 'negro', 'spic', 'beaner', 'chink', 'coon', 'kike', 'wetback', 'sex', 
			'kidnap', 'penis', 'vagina', 'boobs', 'titties', 'sodom', 'kkk', 'nazi', 'klux']

		for word in bad_words:
			if word in username:
				messages.success(request, "We're sorry but some people might find your username offensive. Please pick a different username.")
				return HttpResponseRedirect(reverse('home'))
		if len(username) >= 30:
			messages.error(request, "We're sorry but your username can't be longer than 30 characters")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		gender1 = request.POST['gender']
		day = request.POST['BirthDay']
		month = request.POST['BirthMonth']
		year = request.POST['BirthYear']
		country = request.POST['country']
		state = request.POST['state']
		city = request.POST['city']
		datestr = str(year) + '-' + str(month) + '-' + str(day)
		birthday = datetime.strptime(datestr, '%Y-%m-%d').date()
		user_age = calculate_age(birthday)

		if gender1 == 'm':
			gender = 'Male'
		else:
			gender = 'Female'
			
		try:
			test_year = int(year)
			test_day = int(day)
		except:
			messages.error(request, "Please enter a number for your birthday year and day")
			return render_to_response('profiles/new_user.html', locals(), context_instance=RequestContext(request))

		if user_age >= 18:
			datestr = str(year) + '-' + str(month) + '-' + str(day)
			birthday = datetime.strptime(datestr, '%Y-%m-%d').date()
			user_age = calculate_age(birthday)

			request.user.first_name = first_name
			if len(full_name) >= 2:
				request.user.last_name = last_name
			try: 
				new_info = Info.objects.get(user=request.user)
			except: 
				new_info = Info.objects.create(user=request.user)
			try:
				new_address = Address.objects.get(user=request.user)
			except: 
				new_address = Address.objects.create(user=request.user)
			new_address.country = country
			new_address.state = state
			new_address.city = city
			new_info.gender = gender
			new_info.birthday = birthday
			new_info.signed_up_with_fb_or_goog = False
			new_info.save()
			new_address.save()
			user = authenticate(username=request.user.username, password=request.user.password)
			request.user.save()
			if not DEBUG:
				username = request.user.username
				subject = 'Thanks for registering with Frenvu!'
				plaintext = get_template('registration/email.txt')
				d = Context({ 'username': username })
				text_content = plaintext.render(d)
				msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
				msg.send()
			return HttpResponseRedirect(reverse('handle_new_user'))
		else:
			messages.error(request, "We're sorry but you must be at least 18 to signup!")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('profiles/new_user.html', locals(), context_instance=RequestContext(request))

'''
# this is the second portion of registration for users not signing up with FB or GOOG
def new_user_registration2(request):
	if request.POST:
		name = request.POST['name']
		full_name = name.split()
		first_name1 = str(full_name[0])
		first_name2 = first_name1.translate(None, " '?.!/;:@#$%^&(),[]{}`~-_=+*|<>1234567890")
		first_name = first_name2.translate(None, '"')
		if len(first_name) == 0:
			messages.error(request, "Please use only letters first name")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		if len(full_name) == 2:
			last_name1 = str(full_name[1])
			last_name2 = last_name1.translate(None, "?.!/;:@#$%^&()`,[]{}~_=+*|<>1234567890")
			last_name = last_name2.translate(None, '"')
			if len(last_name) == 0:
				messages.error(request, "Please use only letters in your last name")
				return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		if len(full_name) >= 3:
			not_first_name = full_name[2:len(full_name)]
			last_name0 = full_name[1]
			for name in not_first_name:
				last_name0 = last_name + " " + name
			last_name1 = str(last_name0)
			last_name2 = last_name1.translate(None, "?.!/;:@#$%^&()`,[]{}~_=+*|<>1234567890")
			last_name = last_name2.translate(None, '"')
			if len(last_name) == 0:
				messages.error(request, "Please use only letters in your last name")
				return render_to_response('home.html', locals(), context_instance=RequestContext(request))

		email = request.POST['email']
		try: 
			User.objects.get(email=email)
			messages.error(request, "We're sorry but an account has already been created with this email address")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		except: 
			pass
		gender1 = request.POST['gender']
		day = request.POST['BirthDay']
		month = request.POST['BirthMonth']
		year = request.POST['BirthYear']
		country = request.POST['country']
		state = request.POST['state']
		city = request.POST['city']
		datestr = str(year) + '-' + str(month) + '-' + str(day)
		birthday = datetime.strptime(datestr, '%Y-%m-%d').date()
		user_age = calculate_age(birthday)

		if gender1 == 'm':
			gender = 'Male'
		else:
			gender = 'Female'
			
		try:
			test_year = int(year)
			test_day = int(day)
		except:
			messages.error(request, "Please enter a number for your birthday year and day")
			return render_to_response('profiles/new_user.html', locals(), context_instance=RequestContext(request))

		if user_age >= 18:
			datestr = str(year) + '-' + str(month) + '-' + str(day)
			birthday = datetime.strptime(datestr, '%Y-%m-%d').date()
			user_age = calculate_age(birthday)

			request.user.first_name = first_name
			if len(full_name) >= 2:
				request.user.last_name = last_name
			try: 
				new_info = Info.objects.get(user=request.user)
			except: 
				new_info = Info.objects.create(user=request.user)
			try:
				new_address = Address.objects.get(user=request.user)
			except: 
				new_address = Address.objects.create(user=request.user)
			new_address.country = country
			new_address.state = state
			new_address.city = city
			new_info.gender = gender
			new_info.birthday = birthday
			new_info.signed_up_with_fb_or_goog = False
			new_info.save()
			new_address.save()
			user = authenticate(username=request.user.username, password=request.user.password)
			request.user.save()
			login
			if not DEBUG:
				username = request.user.username
				subject = 'Thanks for registering with Frenvu!'
				plaintext = get_template('registration/email.txt')
				d = Context({ 'username': username })
				text_content = plaintext.render(d)
				msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
				msg.send()
			return HttpResponseRedirect(reverse('handle_new_user'))
		else:
			messages.error(request, "We're sorry but you must be at least 18 to signup!")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('new_user_registration_2.html', locals(), context_instance=RequestContext(request))
'''



'''
The Discover function creates functionality similar to tinder. Users can swipe or use arrow keys or press 
arrows through multiple users. We display their match percentage and all other functionality displayed
on the single user page.
'''



def discover(request):
	preferred_distance = 20
	# first we check to see if a session exists
	username = request.user.username
	'''
	if not request.session.get(username):
		request.session[username] = username
	'''
	# we see if a cache exists
	matches_all = cache.get(username)
	if not matches_all:
		matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).exclude(user1=request.user, user2=request.user).exclude(are_friends=True).filter(distance__lte=preferred_distance)
		# if not, we create a new one
		if matches.count() >= 10:
			matches_all = list(matches)
			cache.set(username, matches_all, 180)
		else:
			matches = Match.objects.filter(
				Q(user1=request.user) | Q(user2=request.user)
				).exclude(user1=request.user, user2=request.user).exclude(are_friends=True)
			matches_all = list(matches)
			cache.set(username, matches_all, 180)
	paginator = Paginator(matches_all, 1)
	
	page = request.GET.get('page')
	try:
		if page != False:
			users = paginator.page(page)
			match = users.object_list[0]

			try:
				match.distance = round(calc_distance(logged_in_user, user))
			except:
				# they have an invalid location
				match.distance = 10000000

			match.percent = match_percentage(match.user1, match.user2)
			match.save()

	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		users = paginator.page(1)

	except EmptyPage:
		#If page is out of range, deliver last page of results
		interests = paginator.page(paginator.num_pages)
 




	return render_to_response('profiles/discover.html', locals(), context_instance=RequestContext(request))





'''
def discover(request):
	# first we check to see if a session exists
	if not request.session.get('random_exp'):
		request.session['random_exp']=1
	# we see if a cache exists
	users_all = cache.get('random_exp_%d' % request.session['random_exp'])
	if not users_all:
		# if not, we create a new one
		users_all = list(User.objects.filter(is_active=True).order_by('?'))
		cache.set('random_exp_%d' % request.session['random_exp'], users_all, 500)
	paginator = Paginator(users_all, 1)
	
	page = request.GET.get('page')
	try:
		if page != False:
			users = paginator.page(page)
			user = users.object_list[0]
			try: 
				assert (user != request.user)
			except: 
				# if the user would go to themselves on pagination, we have them skip a page
				page_int = int(page)
				new_page = page_int + 1
				new_page_u = unicode(new_page)
				users = paginator.page(new_page_u)
				user = users.object_list[0]

			try: 
				match = Match.objects.get(user1=request.user, user2=user)
			except: 
				match, created = Match.objects.get_or_create(user1=user, user2=request.user)
			try:
				match.distance = round(calc_distance(logged_in_user, user))
				if match.distance <= 10:
					match.percent = match_percentage(match.user1, match.user2)
					match.is_10_miles = True
					match.is_20_miles = True 
					match.is_30_miles = True
					match.is_40_miles = True
					match.is_50_miles = True
				elif match.distance <=20:
					match.is_20_miles = True
					match.is_30_miles = True
					match.is_40_miles = True
					match.is_50_miles = True
				elif match.distance <=30:
					match.is_30_miles = True
					match.is_40_miles = True
					match.is_50_miles = True
				elif match.distance <=40:
					match.is_40_miles = True
					match.is_50_miles = True
				elif match.distance <=50: 
					match.is_50_miles = True
			except:
				# they have an invalid location
				match.distance = 10000000

			match.percent = match_percentage(match.user1, match.user2)
			match.save()

			try: 
				assert (match.are_friends == False)
				if match.user1 == request.user: 
					assert (match.user1_approved == False)
				if match.user2 == request.user:
					assert (match.user2_approved == False)
			except: 
				page_int = int(page)
				new_page = page_int + 1
				new_page_u = unicode(new_page)
				users = paginator.page(new_page_u)
				user = users.object_list[0]


	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		users = paginator.page(1)

	except EmptyPage:
		#If page is out of range, deliver last page of results
		interests = paginator.page(paginator.num_pages)
 




	return render_to_response('profiles/discover.html', locals(), context_instance=RequestContext(request))
'''




def friends(request):
	matches = Match.objects.filter(
		Q(user1=request.user) | Q(user2=request.user)
		).filter(are_friends=True)
	number_of_friends = matches.count()
	return render_to_response('profiles/friends.html', locals(), context_instance=RequestContext(request))




#Shows all pictures that the logged in user has 
def all_pictures(request): 
	username = request.user.username
	user = User.objects.get(username=username)
	try: 
		pictures = UserPicture.objects.filter(user=user)
		num_of_pics = pictures.count()
	except: 
		pass
	return render_to_response('profiles/pictures.html', locals(), context_instance=RequestContext(request))




def delete_picture(request, pic_id):
	picture = UserPicture.objects.get(pk=pic_id)
	picture.delete()
	return HttpResponseRedirect(reverse('view_pictures'))




def edit_address(request):
	if request.method == 'POST':

		user = request.user
		addresses = Address.objects.filter(user=user)
		AddressFormSet = modelformset_factory(Address, form=AddressForm, extra=0)
		formset_a = AddressFormSet(request.POST or None, queryset=addresses)

		if formset_a.is_valid():
			for form in formset_a:
				new_form = form.save(commit=False)
				new_form.user = request.user
				new_form.save()
			messages.success(request, 'Your location has been updated.')
		else:
			messages.error(request, 'Please fill out all fields.')
		#return render_to_response('profiles/edit_address.html', locals(), context_instance=RequestContext(request))
		return HttpResponseRedirect('/edit/')
	else:
		raise Http404


def edit_info(request):
	if request.method == 'POST':
		info = Info.objects.get(user=request.user)

		username1 = str(request.POST['username_form'])
		username2 = username1.translate(None, " '?.!/;:@#$%^&(),[]{}`~-=+*|<>")
		username = username2.translate(None, '"')

		bad_words = ['shit', 'cunt', 'fuck', 'nigger', 'kyke', 'dyke', 'fag', 'ass', 'rape', 
				'murder', 'kill', 'gook', 'pussy', 'bitch', 'damn', 'hell', 'whore', 'slut', 
				'cum', 'jizz', 'clit', 'anal', 'cock', 'molest', 'necro', 'satan', 'devil', 
				'pedo', 'negro', 'spic', 'beaner', 'chink', 'coon', 'kike', 'wetback', 'sex', 
				'kidnap', 'penis', 'vagina', 'boobs', 'titties', 'sodom', 'kkk', 'nazi', 'klux']
		for word in bad_words:
			if word in username:
				messages.success(request, "We're sorry but some people might find your username offensive. Please pick a different username.")
				return HttpResponseRedirect(reverse('edit_profile'))


		if len(username) == 0:
			messages.success(request, "Please use only letters and numbers in your username")
			return HttpResponseRedirect(reverse('edit_profile'))



		first_name1 = str(request.POST['first_name_form'])
		first_name2 = first_name1.translate(None, " '?.!/;:@#$%^&(),[]{}`~-_=+*|<>1234567890")
		first_name = first_name2.translate(None, '"')
		if len(first_name) == 0:
			messages.error(request, "Please use only letters first name")
			return HttpResponseRedirect('/edit/')

		last_name1 = str(request.POST['last_name_form'])
		last_name2 = last_name1.translate(None, "?.!/;:@#$%^&()`,[]{}~_=+*|<>1234567890")
		last_name = last_name2.translate(None, '"')
		if len(last_name) == 0:
			messages.error(request, "Please use only letters in your last name")
			return HttpResponseRedirect('/edit/')


		bio = request.POST.get('bio_form')
		gender = request.POST.get('gender_form')
		request.user.username = username
		request.user.first_name = first_name
		request.user.last_name = last_name
		request.user.save()
		info.bio = bio
		info.gender = gender
		info.save()

		messages.success(request, "Profile details updated")
		return HttpResponseRedirect(reverse('edit_profile'))
	else:
		raise Http404



def edit_jobs(request):
	if request.method == 'POST':

		user = request.user
		jobs = Job.objects.filter(user=user)
		JobFormSet = modelformset_factory(Job, form=JobForm, extra=0)
		formset_j = JobFormSet(request.POST or None, queryset=jobs)

		if formset_j.is_valid():
			for form in formset_j:
				new_form = form.save(commit=False)
				new_form.user = request.user
				new_form.save()
			messages.success(request, 'Profile details updated.')
		else:
			messages.error(request, 'Profile details did not update.')
		#return render_to_response('profiles/edit_address.html', locals(), context_instance=RequestContext(request))
		return HttpResponseRedirect('/edit/')
	else:
		raise Http404


def edit_pictures(request):
	if request.method == 'POST':

		user = request.user
		pictures = UserPicture.objects.filter(user=user)
		if pictures.exists():
			PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=0)
		else: 
			PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=1)
		formset_p = PictureFormSet(request.POST or None, request.FILES, queryset=pictures)

		if formset_p.is_valid():
			for form in formset_p:
				new_form = form.save(commit=False)
				image = new_form.image
				if image:
					new_form.user = user
					new_form.save()
			messages.success(request, 'Profile details updated.')
		else:
			messages.error(request, 'Profile details did not update.')
		#return render_to_response('profiles/edit_address.html', locals(), context_instance=RequestContext(request))
		return HttpResponseRedirect('/edit/')
	return render_to_response('profiles/edit_pictures.html', locals(), context_instance=RequestContext(request))


def edit_profile(request):
	user = request.user
	pictures = UserPicture.objects.filter(user=user)
	num_of_pictures = UserPicture.objects.filter(user=user).count()
	addresses = Address.objects.filter(user=user)
	jobs = Job.objects.filter(user=user)
	info = Info.objects.get(user=user)
	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
	direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
	request.session['num_of_messages'] = direct_messages

	if num_of_pictures == 4:
		PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=1)
	elif num_of_pictures == 3:
		PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=2)
	elif num_of_pictures == 2:
		PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=3)
	elif num_of_pictures == 1:
		PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=4)
	elif num_of_pictures == 0:
		PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=5)
	else:
		PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=0)
	formset_p = PictureFormSet(queryset=pictures)

	if addresses.exists():
		AddressFormSet = modelformset_factory(Address, form=AddressForm, extra=0)
		formset_a = AddressFormSet(queryset=addresses)
	else:
		AddressFormSet = modelformset_factory(Address, form=AddressForm, extra=1)
		formset_a = AddressFormSet(queryset=addresses)

	if jobs.exists():
		JobFormSet = modelformset_factory(Job, form=JobForm, extra=0)
		formset_j = JobFormSet(queryset=jobs)
	else:
		JobFormSet = modelformset_factory(Job, form=JobForm, extra=1)
		formset_j = JobFormSet(queryset=jobs)

	

	
	return render_to_response('profiles/edit_profile.html', locals(), context_instance=RequestContext(request))


#sorts the matches of user according to whatver the user specified 
def find_friends(request):
	number_of_users = User.objects.filter(is_active=True).count()
	index_start = randint(1, number_of_users - 5)
	index_end = index_start + 5

	users = User.objects.filter(is_active=True)[index_start:index_end]
	for u in users:
			if u != request.user:
				try: 
					match = Match.objects.get(user1=request.user, user2=u)
				except: 
					match, created = Match.objects.get_or_create(user1=u, user2=request.user)
				match.percent = match_percentage(request.user, u)
				try:
					match.distance = round(calc_distance(request.user, u))
				except:
					match.distance = 10000000
				match.save()
	matches = Match.objects.filter(
		Q(user1=request.user) | Q(user2=request.user)
		)
	return render_to_response('profiles/find_friends.html', locals(), context_instance=RequestContext(request))


def login_user(request):
	try:
		username = request.POST['username']
		password = request.POST['password']

		# check to see whether they provied their username or email for logging in
		if '@' in username:
			kwargs = {'email': username}
		else:
			kwargs = {'username': username}
		user1 = User.objects.get(**kwargs)
		username = user1.username
		user = authenticate(username=username, password=password)

		if user is not None:
			# if user deactivated their account and logged in, they are no longer deactivated
			if user.is_active == False:
				user.is_active = True
				if not DEBUG: 
					subject = 'A user is reactivating their account.'
					message = '%s wants to reactivate their account.' % (username,)
					msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [email])
					msg.content_subtype = "html"
					msg.send()
				messages.succes(request, "We missed you!")
			login(request, user)
			return HttpResponseRedirect(reverse('home'))
		else:
			messages.error(request, "Please double check your username or email address and password")
	except: 
		messages.error(request, "Please double check your username or email address and password")
	return render_to_response('home.html', locals(), context_instance=RequestContext(request))


def logout_user(request):
	logout(request)
	return render_to_response('logout.html', locals(), context_instance=RequestContext(request))


#Calculates a new users age
def calculate_age(born):
	today = date.today()
	try:
		birthday = born.replace(year=today.year)
	except ValueError:
		birthday = born.replace(year=today.year, month=born.month+1, day=1)
	if birthday > today:
		return today.year - born.year -1 
	else:
		return today.year - born.year


#Creates a new user and assigns the appropriate fields to the user (this is for signing up with Frenvu, not FB or Goog)
def register_new_user(request):
	try:
		'''
		username1 = str(request.POST['username'])
		username2 = username1.translate(None, " '?.!/;:@#$%^&(),[]{}`~-_=+*|<>")
		username = username2.translate(None, '"')
		if len(username) == 0:
			messages.error(request, "Please use only letters and numbers in your username")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		'''


		email = str(request.POST['email'])

		if '@' not in email:
			messages.success(request, 'Please provide a valid email address')
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))

		email_as_username = email.translate(None, " '?.!/;:@#$%^&(),[]{}`~-_=+*|<>")
		if len(email_as_username) == 0:
			messages.error("Please provide a valid email")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		password = request.POST['password']
		confirm_password = request.POST['repassword']



		if email and password:
				if password == confirm_password:
					try:
						new_user,created = User.objects.get_or_create(username=email_as_username, password=password)
					except:	
						messages.error(request, "Sorry but this username is already taken")
						return render_to_response('home.html', locals(), context_instance=RequestContext(request))
					if created:
						new_user.set_password(password)
						
						new_user.save()
						new_user = authenticate(username=email_as_username, password=password)
						login(request, new_user)
						return HttpResponseRedirect(reverse('new_user_info'))
				else:
					messages.error(request, "Please make sure both passwords match")
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))
	except:		
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))



#Displays the profile page of a specific user and their match % against the logged in user
def single_user(request, username):
	try:
		user = User.objects.get(username=username)
		if user.is_active:
			single_user = user
	except:
		raise Http404
	try: 
		if single_user != request.user:
			try: 
				match = Match.objects.get(user1=request.user, user2=single_user)
			except: 
				match, created = Match.objects.get_or_create(user1=single_user, user2=request.user)
			match.percent = match_percentage(request.user, single_user)
			try:
				match.distance = round(calc_distance(request.user, user))
			except:
				match.distance = 10000000
			match.save()
			interests_all = Interest.objects.filter(userinterestanswer__user=single_user)
			pictures = UserPicture.objects.filter(user=single_user)

	except: 
		raise Http404
	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
	direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
	request.session['num_of_messages'] = direct_messages

	
	return render_to_response('profiles/single_user.html', locals(), context_instance=RequestContext(request))	


def single_user_pictures(request, username):
	pictures = UserPicture.objects.filter(user__username=username)
	return render_to_response('profiles/single_user_pictures.html', locals(), context_instance=RequestContext(request))



def search(request):
	try:
		q = request.GET.get('q', '')
	except: 
		q = False
	users_queryset = User.objects.filter(
		Q(username__icontains=q)
		)
	results = users_queryset
	return render_to_response('search.html', locals(), context_instance=RequestContext(request))



def terms_and_agreement(request): 
	return render_to_response('terms.html', locals(), context_instance=RequestContext(request))


def delete_picture(request, pic_id):
	user = request.user
	pic = UserPicture.objects.filter(user=user).get(id=pic_id)
	pic.delete()
	return HttpResponseRedirect(reverse('pictures'))


def delete_account(request):
	username = request.user.username
	deactivated_user = User.objects.get(username=username)
	deactivated_user.is_active = False
	logout(request)
	messages.success(request, "Your account has been deactivated. Your account will be deleted in 30 days.")
	messages.success(request, "We're sorry to see you go, but if you change your mind before then, just log back in to reactivate it!")
	if not DEBUG: 
		subject = 'A user is deactivating their account.'
		message = '%s wants to delete their account.' % (username,)
		msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [email])
		msg.content_subtype = "html"
		msg.send()

	return render_to_response('home.html', locals(), context_instance=RequestContext(request))


def contact_us(request):
	if request.POST:
		user = User.objects.get(username=request.user.username)
		message1 = user.username + " has an inquiry:"
		message2 = request.POST['message']
		message = message1 + message2
		send_mail('Inquiry', message , EMAIL_HOST_USER, [EMAIL_HOST_USER])
		messages.success(request, "Your inquiry has been sent, and we'll get back to you as soon as we can!")
	return render_to_response ('contact_us.html', locals(), context_instance=RequestContext(request))


def new_picture(request):
	if request.method == 'POST':
		pic_form = UserPictureForm(request.POST, request.FILES)
		if pic_form.is_valid():
			form = pic_form.save(commit=False)
			image = pic_form.cleaned_data["image"]
			if image:
				form.user = request.user
				form.image = image
				form.save()
	return HttpResponseRedirect(reverse('pictures'))



def ice_breaker(request): 
	user1 = request.user
	user1_interests = UserInterestAnswer.objects.filter(user=user1).filter(
		Q(importance_level="Like") | Q(importance_level="Strongly Like"))
	if user1_interests.count() == 0:
		messages.success(request, "We're sorry, but you need to like a few interests first!")
		return HttpResponseRedirect(reverse('home'))
	max_interest = user1_interests.latest('id').id
	max_user = User.objects.latest('id').id

	#we keep iterating through until we find an interest that the logged in user either liked or strongly liked
	while True: 
		try:
			random_interest = user1_interests.get(pk=randint(1, max_interest))
			assert (random_interest.importance_level == "Strongly Like" or random_interest.importance_level == "Like")
			break
		except: 
			pass
	# we keep iterating until we find a user that either liked or strongly liked the interested we found in previous loop
	while True: 
		try: 
			random_user = User.objects.get(pk=randint(1, max_user))
			assert (user1 != random_user)
			#random_info = Info.objects.get(user=random_user)
			#assert (random_info.is_new_user == False)
			same_interest = UserInterestAnswer.objects.filter(user=random_user).get(interest=random_interest.interest)
			assert (same_interest.importance_level == "Strongly Like" or same_interest.importance_level == "Like") 
			break
		except:
			pass
	try: 
		match = Match.objects.get(user1=request.user, user2=random_user)
		user1 = request.user
		user2 = random_user
	except:
		match, created = Match.objects.get_or_create(user1=random_user, user2=request.user)
		user1 = random_user
		user2 = request.user
	match.user1_approved = True
	match.user2.approved = True

	subject = "You two have an interest in common!"
	body_for_user1 = "You and %s both like %s! What exactly is it about %s that you like so much? Let %s know your thoughts! " %(user2.username, random_interest, random_interest, user2.username)
	body_for_user2 = "You and %s both like %s! What exactly is it about %s that you like so much? Let %s know your thoughts! " %(user1.username, random_interest, random_interest, user1.username)
	user1_message = DirectMessage.objects.create(subject=subject, body=body_for_user1, receiver=user1, sender=user2)
	user2_message = DirectMessage.objects.create(subject=subject, body=body_for_user2, receiver=user2, sender=user1)
	user1_message.sent = datetime.now()
	user2_message.sent = datetime.now()
	user1_message.save()
	user2_message.save()
	user_gamification = Gamification.objects.get(user=request.user)
	user_gamification.icebreaker_until_reset = datetime.now() + timedelta(hours=3)
	user_gamification.save()
	messages.success(request, "Please check your inbox, we've found a user that you have an interest in common with!")
	return HttpResponseRedirect(reverse('home'))








