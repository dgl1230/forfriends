# -*- coding: utf-8 -*-
import operator 
import datetime
import random
from datetime import date, datetime, timedelta
import logging
from random import randint

from django.shortcuts import render
from django.contrib import messages, auth
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.db.models import Q, Max
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.clickjacking import xframe_options_exempt




from forfriends.settings.deployment import EMAIL_HOST_USER, DEBUG, MEDIA_URL
from forfriends.matching import match_percentage, find_same_interests
from forfriends.distance import calc_distance, check_valid_location, find_nearby_users
from forfriends.s3utils import delete_s3_pic
from matches.models import Match
from .models import Address, Job, Info, UserPicture, Gamification
from .forms import AddressForm, InfoForm, JobForm, UserPictureForm
from interests.models import UserInterestAnswer, Interest
from directmessages.models import DirectMessage
from questions.models import Question, UserAnswer




CURRENTLY_LOCALLY_TESTING = False

def custom_show_toolbar(request):
	return True



def user_not_new(user):
	try: 
		user_info = Info.objects.get(user=user)
	except:
		return False
	return user.is_authenticated() and user_info.signed_up_with_fb_or_goog == False and user_info.is_new_user == False

'''
def user_can_reset_circle(user):
	try: 
		user_gamification = Gamification.objects.get(user=request.user)
	except:
		return False
	try:
		until_next_reset = user_gamification.circle_time_until_reset
	except:
		user_gamification.circle_time_until_reset = datetime.now()
	until_next_reset = user_gamification.circle_time_until_reset.replace(tzinfo=None)
	hours_until_reset = int((until_next_reset - current_time).total_seconds() / 60 / 60)
	return hours_until_reset <= 1
'''


def user_can_reset_icebreaker(user):
	try: 
		user_gamification = Gamification.objects.get(user=request.user)
	except:
		return False
	try:
		until_next_icebreaker = user_gamification.icebreaker_until_reset.replace(tzinfo=None)
	except:
		user_gamification.icebreaker_until_reset = datetime.now()
	until_next_icebreaker = user_gamification.icebreaker_until_reset.replace(tzinfo=None)
	icebreaker_hours_until_reset = int((until_next_icebreaker - current_time).total_seconds() / 60 / 60)
	return icebreaker_hours_until_reset <= 0





'''Implements the 'add friend' button when viewing a user's profile
If both users click this button on each other's profile, they can message'''
@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def add_friend(request, username):
	try: 
		match = Match.objects.get(user1=request.user, user2__username=username)
		match.user1_approved = True
	except: 
		match, created = Match.objects.get_or_create(user1__username=username, user2=request.user)
		match.user2_approved = True

	if (match.user1 == request.user and match.user1_approved == True and match.user2_approved == False):
		if not CURRENTLY_LOCALLY_TESTING: 
			sender = User.objects.get(username="TeamFrenvu")
		else: 
			sender = request.user
		requested= match.user2
		subject = "Someone wants to be your friend!"
		body = "Hey %s, %s thinks you two could be pretty good friends! Why don't you check out their profile and see if you think they seem cool? " %(requested, request.user.username)
		message = DirectMessage.objects.create(subject=subject, body=body, sender=sender, receiver=requested)
		match.save()
		message.save()


	if (match.user2 == request.user and match.user2_approved == True and match.user1_approved == False):
		if not CURRENTLY_LOCALLY_TESTING: 
			sender = User.objects.get(username="TeamFrenvu")
		else: 	
			sender = request.user
		requested= match.user1
		subject = "Someone wants to be your friend!"
		body = "Hey %s, %s thinks you two could be pretty good friends! Why don't you check out their profile and see if you think they seem cool?" %(requested, request.user.username)
		message = DirectMessage.objects.create(subject=subject, body=body, sender=sender,receiver=requested)
		match.save()
		message.save()


	if (match.user1_approved == True and match.user2_approved == True):
		if not CURRENTLY_LOCALLY_TESTING: 
			sender1 = User.objects.get(username="TeamFrenvu")
			sender2 = User.objects.get(username="TeamFrenvu")
		else:
			sender1 = match.user1
			sender2 = match.user2
		user1 = match.user1
		user2 = match.user2
		match.are_friends = True
		subject = "You have a new friend!"
		body_for_user1 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user2.username)
		body_for_user2 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user1.username)
		user1_message = DirectMessage.objects.create(subject=subject, body=body_for_user1, receiver=sender1)
		user2_message = DirectMessage.objects.create(subject=subject, body=body_for_user2, receiver=sender2)
		user1_message.sent = datetime.now()
		user2_message.sent = datetime.now()
		match.save()
		user1_message.save()
		user2_message.save()
		
	
	single_user = User.objects.get(username=username)
	match.save()
	if not CURRENTLY_LOCALLY_TESTING:
		return HttpResponseRedirect('http://www.frenvu.com/members/%s' % username)
	else: 
		return HttpResponseRedirect('http://127.0.0.1:8000/members/%s' % username)
	
	return render_to_response('profiles/single_user.html', locals(), context_instance=RequestContext(request))


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def add_friend_discovery(request, username, page):
	try: 
		match = Match.objects.get(user1=request.user, user2__username=username)
		match.user1_approved = True
	except: 
		match, created = Match.objects.get_or_create(user1__username=username, user2=request.user)
		match.user2_approved = True

	if (match.user1 == request.user and match.user1_approved == True and match.user2_approved == False):
		
		if not CURRENTLY_LOCALLY_TESTING: 
			sender = User.objects.get(username="TeamFrenvu")
		else: 	
			sender = request.user
		requester = request.user
		requested= match.user2
		subject = "Someone wants to be your friend!"
		body = "Hey %s, I think we could be pretty good friends! Why don't you check out my profile and see if you think we'd get along?" %(requested)
		message = DirectMessage.objects.create(subject=subject, body=body, sender=sender, receiver=requested)
		message.save()
		
		match.save()
		


	if (match.user2 == request.user and match.user2_approved == True and match.user1_approved == False):
		
		if not CURRENTLY_LOCALLY_TESTING: 
			sender = User.objects.get(username="TeamFrenvu")
		else: 	
			sender = request.user
		requester = request.user
		requested= match.user1
		subject = "Someone wants to be your friend!"
		body = "Hey %s, I think we could be pretty good friends! Why don't you check out my profile and see if you think we'd get along?" %(requested)
		message = DirectMessage.objects.create(subject=subject, body=body, sender=sender,receiver=requested)
		match.save()
		message.save()
		
		match.save()



	if (match.user1_approved == True and match.user2_approved == True):
		if not CURRENTLY_LOCALLY_TESTING: 
			sender1 = User.objects.get(username="TeamFrenvu")
			sender2 = User.objects.get(username="TeamFrenvu")
		else:
			sender1 = match.user1
			sender2 = match.user2
		user1 = match.user1
		user2 = match.user2
		match.are_friends = True
		subject = "You have a new friend!"
		body_for_user1 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user2.username)
		body_for_user2 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user1.username)
		user1_message = DirectMessage.objects.create(subject=subject, body=body_for_user1, receiver=user1, sender=sender1)
		user2_message = DirectMessage.objects.create(subject=subject, body=body_for_user2, receiver=user2, sender=sender2)
		user1_message.sent = datetime.now()
		user2_message.sent = datetime.now()
		match.save()
		user1_message.save()
		user2_message.save()
		
	
	single_user = User.objects.get(username=username)
	match.save()
	messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
	direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
	request.session['num_of_messages'] = direct_messages
	if not CURRENTLY_LOCALLY_TESTING:
		return HttpResponseRedirect('http://www.frenvu.com/discover/?page=%s' % page)
	else: 
		return HttpResponseRedirect('http://127.0.0.1:8000/discover/?page=%s' % page)


'''
The view for the home page of a user. If they're logged in and not a new user, 
it shows their crowd. If they're logged in and a new user, it redirects them to handle_new_user, 
which will have the user fill in relevant info before they can access the site. Otherwise, 
the user is not logged in, and is shown the landing page.
'''

@xframe_options_exempt
def all(request):
	if request.user.is_authenticated():
		info, created = Info.objects.get_or_create(user=request.user)
		
		try: 
			if info.signed_up_with_fb_or_goog == True:
				return HttpResponseRedirect(reverse('new_user_info'))

			if info.is_new_user == True:
				#is_new_user = True
				return HttpResponseRedirect(reverse('new_user_info'))
			user_interests = UserInterestAnswer.objects.filter(user=request.user)
			user_questions = UserAnswer.objects.filter(user=request.user)
			if user_interests.count() >= 5 and user_questions.count() >= 10:
				can_make_first_crowd = True
				#info.is_new_user = False
				#info.save()
				#is_new_user = False
			else:
				can_make_first_crowd = False
				#return render_to_response('all.html', locals(), context_instance=RequestContext(request))
		except: 
			pass
		if info.is_new_user == False:
			is_new_user = False

			'''
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
						return HttpResponseRedirect(reverse('generate_circle'))
				# if the user has multiple circles, we delete all of their circles
				if number_of_circles > 1:
					user_gamification.delete()
			except:
				pass
			'''

			# this is to see if the user has a circle

			try: 
				user_gamification = Gamification.objects.get(user=request.user)
			except: 
				#user does not have a circle
				
				user_gamification = Gamification.objects.create(user=request.user)
				user_gamification.circle_time_until_reset = datetime.now()
				user_gamification.icebreaker_until_reset = datetime.now()
				user_gamification.save()
				#return HttpResponseRedirect(reverse('generate_circle'))
			try:
				# check and see if the user has any value in their circle fields
				until_next_reset = user_gamification.circle_time_until_reset
				until_next_icebreaker = user_gamification.icebreaker_until_reset
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
			#try to get their current icebreaker match
			try:
				icebreaker_match = Match.objects.get(Q(user1=request.user, currently_in_icebreaker_user1=True) | Q(user2=request.user, currently_in_icebreaker_user2=True))
				
				if can_reset_icebreaker == True: 
					if icebreaker_match.currently_in_icebreaker_user1 == True and icebreaker_match.user1 == request.user: 
						icebreaker_match.currently_in_icebreaker_user1 = False
						icebreaker_match.save()
					else:
						icebreaker_match.currently_in_icebreaker_user2 = False
						icebreaker_match.save()
			except: 
				pass
		return render_to_response('all.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def generate_circle(request):
	#start_time = datetime.now()
	location = Address.objects.get(user=request.user)
	if check_valid_location(location.city, location.state) == False:
		messages.success(request, "We're sorry but you need to enter a valid location before you can use discover")
		return HttpResponseRedirect(reverse('home'))

	#change
	info = Info.objects.get(user=request.user)
	if info.is_new_user:
		info.is_new_user = False
		info.save()
	num_of_matches = matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).count()
	#time1 = datetime.now()
	if num_of_matches < 7:
		users = User.objects.filter(is_active=True).exclude(username=request.user.username).order_by('?')
		i = 0
		for user in users: 
			if i == 7:
				break
			if user != request.user:
				try: 
					match = Match.objects.get(user1=request.user, user2=user)
				except: 
					match, created = Match.objects.get_or_create(user1=user, user2=request.user)
				try:
					match.distance = round(calc_distance(request.user, user))
				except:
					match.distance = 10000000
				match.save()
				i = i + 1


	preferred_distance = 15
	#these variables are for keeping track of users that live within certain miles, ie num_10m is 
	# for users that live within 10 miles

	# these blocks can lead to a lot of unnecessary querying evaluations
	if circle_distance(request.user, preferred_distance) == 1:
		return HttpResponseRedirect(reverse('home'))
	
	elif circle_distance(request.user, unicode(int(preferred_distance) + 10)) == 1:
		return HttpResponseRedirect(reverse('home'))
	elif circle_distance(request.user, unicode(int(preferred_distance) + 20)) == 1:
		return HttpResponseRedirect(reverse('home'))
	elif circle_distance(request.user, unicode(int(preferred_distance) + 30)) == 1:
		return HttpResponseRedirect(reverse('home'))
	
	
	# otherwise, there are not very many users who live close by, so we default to 
	# adding to their circle randomly
	user_gamification = Gamification.objects.get(user=request.user)
	current_circle = list(user_gamification.circle.all())
	
	# for now are_friends=True is excluded from other queries because in theory all friends should be in requested users
	requested_users = list(Match.objects.filter(Q(user1=request.user, user1_approved=True) | Q(user2=request.user, user2_approved=True )))
	excluded_users = current_circle + requested_users
	
	
	matches = Match.objects.filter(
		Q(user1=request.user) | Q(user2=request.user)
		).exclude(user1=request.user, user2=request.user).exclude(id__in=[o.id for o in excluded_users])	
	if matches.count() < 6:
		matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).exclude(user1=request.user, user2=request.user)
	

	# so we dont have more than 6-7 users in a circle at a time
	user_gamification.circle.clear()
	temp_list = []
	for i in range(matches.count()):
		temp_list.append(i)
	for i in range(6):
		index = choose_and_remove(temp_list)
		random_match = matches[index]
		user_gamification.circle.add(random_match)
	user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
	user_gamification.save()
	return HttpResponseRedirect(reverse('home'))


def choose_and_remove(items):
	if items:
		index = random.randrange(len(items))
		return items.pop(index)
	return None

	



def circle_distance(logged_in_user, preferred_distance):
	#start_time = datetime.now()
	user_gamification = Gamification.objects.get(user=logged_in_user)
	current_circle = list(user_gamification.circle.all())
	#need try catch here
	team_frenvu = User.objects.get(username="TeamFrenvu")
	current_circle.append(team_frenvu)

	matches = Match.objects.filter(
		Q(user1=logged_in_user) | Q(user2=logged_in_user)
		).exclude(user1=logged_in_user, user2=logged_in_user).exclude(are_friends=True).filter(percent__gte=70).exclude(id__in=[o.id for o in current_circle]).filter(distance__lte=preferred_distance)
	count = matches.count()
	if matches.count() < 7:
		return 0
	already_chosen = {}
	user_gamification.circle.clear()
	#max_match = matches.latest('id').id

	temp_list = []
	for i in range(matches.count()):
		temp_list.append(i)
	for i in range(6):
		index = choose_and_remove(temp_list)
		random_match = matches[index]
		user_gamification.circle.add(random_match)
	user_gamification.circle_reset_started = datetime.now()
	user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
	user_gamification.save()
	return 1


def first_circle(logged_in_user):
	user_gamification = Gamification.objects.create(user=logged_in_user)
	users = User.objects.filter(is_active=True).exclude(username=logged_in_user.username)
	i = 0
	for user in users: 
		if i > 7:
			break
		if user != logged_in_user:
			try: 
				match = Match.objects.get(user1=logged_in_user, user2=user)
			except: 
				match, created = Match.objects.get_or_create(user1=user, user2=logged_in_user)
			try:
				match.distance = round(calc_distance(logged_in_user, user))
			except:
				match.distance = 10000000
			if match.distance <= 20:
				match.percent = match_percentage(logged_in_user, single_user)
				if match.percent >=70:
					i += 1

			match.save()

		matches = Match.objects.filter(
			Q(user1=logged_in_user) | Q(user2=logged_in_user)
			).exclude(are_friends=True).filter(percent__gte=70)
		num_matches = matches.count()
		if num_matches >= 7:
			matches_new = matches.order_by('?')[:8]
			i = 0
			for match in matches:
				if match.user1 == logged_in_user and match.user2 == logged_in_user:
					pass
				else:
					i += 1
					user_gamification.circle.add(match)
					if i == 7:
						break
		else:
			matches = Match.objects.filter(
				Q(user1=logged_in_user) | Q(user2=logged_in_user)
				).exclude(are_friends=True)
			matches_new = matches.order_by('?')[:8]
			i = 0
			for match in matches_new:
				if match.user1 == logged_in_user and match.user2 == logged_in_user:
					pass
				else:
					i += 1
					user_gamification.circle.add(match)
					if i == 7:
						break
		
		user_gamification.circle_time_until_reset = datetime.now()
		user_gamification.icebreaker_until_reset = datetime.now()
		user_gamification.save()
		return HttpResponseRedirect(reverse('home'))


def new_user_fb_or_goog(request, email):
	if request.POST:
		username1 = str(request.POST['username'])
		username2 = username1.translate(None, " '?.!/;:@#$%^&(),[]{}`~-=+*|<>")
		username = username2.translate(None, '"')
		bad_words = ['shit', 'cunt', 'fuck', 'nigger', 'kyke', 'dyke', 'fag', 'ass', 'rape', 
				'murder', 'kill', 'gook', 'pussy', 'bitch', 'whore', 'slut', 
				'cum', 'jizz', 'clit', 'anal', 'cock', 'molest', 'necro', 'satan', 'devil', 
				'pedo', 'negro', 'spic', 'beaner', 'chink', 'coon', 'kike', 'wetback', 'sex', 
				'kidnap', 'penis', 'vagina', 'boobs', 'titties', 'sodom', 'kkk', 'nazi', 'klux', 
				'dicksucker', 'rapist', 'anus', 'arse', 'bastard','blowjob', 
				'boner', 'fister', 'butt', 'cameltoe', 'chink', 'coochie', 'coochy', 'bluewaffle', 
				'cooter', 'dick', 'dildo', 'doochbag', 'douche', 'fellatio', 'feltch', 'flamer', 
				'donkeypunch', 'fudgepacker', 'gooch', 'gringo', 'jerkoff', 'jigaboo', 'kooch', 
				'kootch', 'kunt', 'kyke', 'dike', 'minge', 'munging', 'nigga', 'niglet', 'nutsack', 
				'poon', 'pussies', 'pussy', 'queef', 'queer', 'rimjob', 'erection', 'schlong', 
				'skeet', 'smeg', 'spick', 'splooge', 'spook', 'retard', 'testicle', 'twat', 
				'vajayjay', 'wankjob', 'bimbo', '69', 'fistr', 'fist3r']

		for word in bad_words:
			if word in username:
				messages.success(request, "We're really sorry, but some people might find your username offensive. Please pick a different username.")
				return HttpResponseRedirect(reverse('home'))
		if len(username) >= 30:
			messages.error(request, "We're sorry but your username can't be longer than 30 characters")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		day = request.POST['BirthDay']
		month = request.POST['BirthMonth']
		year = request.POST['BirthYear']
		country = request.POST['country']
		state = request.POST['state']
		city = request.POST['city'].title()
		datestr = str(year) + '-' + str(month) + '-' + str(day)
		birthday = datetime.strptime(datestr, '%Y-%m-%d').date()
		user_age = calculate_age(birthday)
		try:
			test_year = int(year)
			test_day = int(day)
		except:
			messages.error(request, "Please enter a number for your birthday year and day")
			return render_to_response('profiles/new_user.html', locals(), context_instance=RequestContext(request))

		if user_age >= 18:
			#datestr = str(year) + '-' + str(month) + '-' + str(day)
			birthday = datetime.strptime(datestr, '%Y-%m-%d').date()
			user_age = calculate_age(birthday)
			new_user = User.objects.get(email=email)
			try: 
				new_info = Info.objects.get(user=new_user)
			except: 
				new_info = Info.objects.create(user=new_user)
			try:
				new_address = Address.objects.get(user=new_user)
			except: 
				new_address = Address.objects.create(user=new_user)
			new_address.country = country
			new_address.state = state
			new_address.city = city
			new_info.birthday = birthday
			new_info.signed_up_with_fb_or_goog = False
			new_info.is_new_user = False
			new_info.save()
			new_address.save()
			try: 
				user = User.objects.get(username=username)
				messages.error(request, "We're sorry, but that user name is already taken!")
				return HttpResponseRedirect(reverse('home'))
			except:
				pass
			new_user.username = username
			#request.user.is_active = True
			new_user.save()
			user = authenticate(username=new_user.username, password=new_user.password)
			new_user.save()


			if not CURRENTLY_LOCALLY_TESTING:

				subject = "Welcome to Frenvu!"
				line1 = "Thanks for signing up %s! Frenvu is a place where you can find your closest friends, someone cool to see a movie with," % (request.user.username)
				line2 = " or anything in between. After you answer some interests and questions, try creating a crowd to find 6 potential friends who live close by."
				line3 = " Or you could do an icebreaker, and we'll start a conversation with another user you share an interest with! There's plenty more to do as well,"
				line4 = " and we are constantly working on additional features. If you have any questions or concerns, please let us know! We want Frenvu to be the most fun"
				line5 = " and welcoming place for you to meet new people. We hope you enjoy the site!" + '\n' + '\n'
				line6 = " - The Team at Frenvu "
				body = line1 + line2 + line3 + line4 + line5 + line6
				sender = User.objects.get(username="TeamFrenvu")
				new_user_welcome_message = DirectMessage.objects.create(subject=subject, body=body, receiver=request.user, sender=sender, sent=datetime.now())
				new_user_welcome_message.save()

				email = request.user.email
				username = request.user.username
				subject = 'Thanks for registering with Frenvu!'
				plaintext = get_template('registration/email.txt')
				d = Context({ 'username': username })
				text_content = plaintext.render(d)
				msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
				msg.send()
			return HttpResponseRedirect(reverse('home'))
		else:
			messages.error(request, "We're sorry but you must be at least 18 to signup!")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('new_user_registration_2.html', locals(), context_instance=RequestContext(request))





	
@login_required(login_url=reverse_lazy('home'))
#This is the first/second part of registration for users signing up with FB or GOOGerror(request, "Please double check your username or email address and password")
def new_user_info(request):
	if request.POST:
		first_name1 = str(request.POST['first_name'])
		first_name2 = first_name1.translate(None, " '?.!/;:@#$%^&(),[]{}`~-_=+*|<>1234567890")
		first_name = first_name2.translate(None, '"')

		

		if len(first_name) == 0:
			messages.error(request, "Please use only letters first name")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))

		last_name_string = str(request.POST['last_name']).split()
				
		last_name = ""
		for name in last_name_string:
			last_name = last_name + str(name) + " "
		last_name1 = last_name.translate(None, "?.!/;:@#$%^&()`,[]{}~_=+*|<>1234567890")
		last_name = last_name1.translate(None, '"')
		if len(last_name) == 0:
			messages.error(request, "Please use only letters in your last name")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
		username1 = str(request.POST['username'])

		username2 = username1.translate(None, " '?.!/;:@#$%^&(),[]{}`~-=+*|<>")
		username = username2.translate(None, '"')

		bad_words = ['shit', 'cunt', 'fuck', 'nigger', 'kyke', 'dyke', 'fag', 'ass', 'rape', 
			'murder', 'kill', 'gook', 'pussy', 'bitch', 'whore', 'slut', 
			'cum', 'jizz', 'clit', 'anal', 'cock', 'molest', 'necro', 'satan', 'devil', 
			'pedo', 'negro', 'spic', 'beaner', 'chink', 'coon', 'kike', 'wetback', 'sex', 
			'kidnap', 'penis', 'vagina', 'boobs', 'titties', 'sodom', 'kkk', 'nazi', 'klux', 
			'dicksucker', 'rapist', 'anus', 'arse', 'bastard','blowjob', 
			'boner', 'fister', 'butt', 'cameltoe', 'chink', 'coochie', 'coochy', 'bluewaffle', 
			'cooter', 'dick', 'dildo', 'doochbag', 'douche', 'fellatio', 'feltch', 'flamer', 
			'donkeypunch', 'fudgepacker', 'gooch', 'gringo', 'jerkoff', 'jigaboo', 'kooch', 
			'kootch', 'kunt', 'kyke', 'dike', 'minge', 'munging', 'nigga', 'niglet', 'nutsack', 
			'poon', 'pussies', 'pussy', 'queef', 'queer', 'rimjob', 'erection', 'schlong', 
			'skeet', 'smeg', 'spick', 'splooge', 'spook', 'retard', 'testicle', 'twat', 
			'vajayjay', 'wankjob', 'bimbo', '69', 'fistr', 'fist3r']

		for word in bad_words:
			if word in username:
				messages.success(request, "We're really sorry, but some people might find your username offensive. Please pick a different username.")
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
		city = request.POST['city'].title()
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
			new_info.is_new_user = False
			new_info.save()
			new_address.save()
			try: 
				user = User.objects.get(username=username)
				messages.error(request, "We're sorry, but that user name is already taken!")
				return HttpResponseRedirect(reverse('home'))
			except:
				pass
			#request.user.username = username
			#request.user.first_name = first_name
			#request.user.last_name = last_name
			
			
			
			request.user.save()
			user = authenticate(username=request.user.username, password=request.user.password)
			#user.save()
			new_user = User.objects.get(username=request.user.username)
			new_user.username = username
			new_user.first_name = first_name
			new_user.last_name = last_name
			new_user.save()



			if not CURRENTLY_LOCALLY_TESTING:

				subject = "Welcome to Frenvu!"
				line1 = "Thanks for signing up %s! Frenvu is a place where you can find your closest friends, someone cool to see a movie with," % (request.user.username)
				line2 = " or anything in between. After you answer some interests and questions, try creating a crowd to find 6 potential friends who live close by."
				line3 = " Or you could do an icebreaker, and we'll start a conversation with another user you share an interest with! There's plenty more to do as well,"
				line4 = " and we are constantly working on additional features. If you have any questions or concerns, please let us know! We want Frenvu to be the most fun"
				line5 = " and welcoming place for you to meet new people. We hope you enjoy the site!" + '\n' + '\n'
				line6 = " - The Team at Frenvu "
				body = line1 + line2 + line3 + line4 + line5 + line6
				sender = User.objects.get(username="TeamFrenvu")
				new_user_welcome_message = DirectMessage.objects.create(subject=subject, body=body, receiver=request.user, sender=sender, sent=datetime.now())
				new_user_welcome_message.save()

				email = request.user.email
				username = request.user.username
				subject = 'Thanks for registering with Frenvu!'
				plaintext = get_template('registration/email.txt')
				d = Context({ 'username': username })
				text_content = plaintext.render(d)
				msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
				msg.send()
			return HttpResponseRedirect(reverse('home'))
		else:
			messages.error(request, "We're sorry but you must be at least 18 to signup!")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('profiles/new_user.html', locals(), context_instance=RequestContext(request))


def user_not_new(user):
	try: 
		user_info = Info.objects.get(user=user)
	except:
		return False
	return user.is_authenticated() and user_info.signed_up_with_fb_or_goog == False


#san_francico_area = ['San Francisco']
#south_san_francisco = ['Daly City', 'Brisbane', 'South San Francisco', 








def create_user_list(logged_in_user):
	user_gamification = Gamification.objects.get(user=logged_in_user)
	users_all = User.objects.filter(is_active=True)
	current_location = Address.objects.get(user=logged_in_user)
	current_state = current_location.state
	current_city = current_location.city
	close_by_users = list(User.objects.filter(address__state=current_state).filter(address__city=current_city).exclude(username=logged_in_user.username))
	excluded_users = []
	matches = Match.objects.filter(
		Q(user1=logged_in_user, user1_approved=True) | Q(user2=logged_in_user, user2_approved=True)
		)
	excluded_users.append(logged_in_user)
	for match in matches:
		if match.user1 != logged_in_user:
			excluded_users.append(match.user1)
		else:
			excluded_users.append(match.user2)

	new_users = [x for x in close_by_users if x not in excluded_users]
	user_gamification.discover_list = new_users
	user_gamification.save()


def redo_user_list(logged_in_user):
	user_gamification = Gamification.objects.get(user=logged_in_user)
	matches = Match.objects.filter(
		Q(user1=logged_in_user) | Q(user2=logged_in_user)
		)
	for match in matches:
		if match.user1 != logged_in_user:
			user_list.append(match.user1)
		else:
			user_list.append(match.user2)
	#save user list

def find_close_cities(city):

	oakland = ['Oakland', 'San Francisco', 'Alameda', 'Emeryville', 'Piedmont', 'Berkeley']
	san_francisco = ['San Francisco', 'Daly City', 'Brisbane']
	daly_city = ['San Francisco', 'South San Francisco', 'Pacifica', 'San Bruno', 'Daly City', 'Brisbane']
	south_san_francisco = ['Daly City', 'South San Francisco', 'Pacifica', 'Millbrae', 'Brisbane']
	pacifica = ['Pacifica', 'Daly City', 'South San Francisco', 'San Bruno']
	san_bruno = ['South San Francisco', 'Brisbane','San Bruno', 'Millbrae']
	#hillsborough and burlingham included with millbrae
	millbrae = ['San Bruno', 'Millbrae', 'Hillsborough', 'Burlingame', 'South San Francisco', 'San Mateo']
	#foster city, highlands-baywood park can be included here
	san_mateo= ['San Mateo', 'Hillsborough', 'Burlingame', 'Foster City', 'Belmont', 'Highlands-Baywood Park']
	#Belmont, San Carlos, Emerald Hills, 'North Fair Oaks, Woodside, Atherton
	redwood_city = ['Redwood City', 'Belmont', 'San Carlos', 'Emerald Hills', 'North Fair Oaks', 'Atherton', 'Menlo Park', 
						'West Menlo Park', 'Palo Alto', 'Stanford', 'East Palo Alto', 'Portola Valley', 'Woodside']
	#for Palo Alto, Menlo Park, Portola Valley, West Menlo Park, Stanford
	between_redwood_and_mountainview = ['Redwood City', 'Woodside', 'Emerald Hills', 'North Fair Oaks', 'Atherton', 
					'Menlo Park', 'West Menlo Park', 'Palo Alto', 'Portola Valley', 'Stanford', 'East Palo Alto']
	#covers mountain view, los altos, SunnyVale, Loyola, Cupertino
	mountainview = ['Mountain View', 'Los Altos', 'Sunnyvale', 'Palo Alto', 'Stanford', 'Santa Clara']
	#Includes San Jose, Santa Clara, Campbell, Cupertino, Milpitas, Cambrian Park, Milpitas, East Foothills
	san_jose = ['San Jose', 'Santa Clara', 'Campbell', 'Cupertino', 'Milpitas', 'Cambrian Park', 'Mountain View', 
				'Los Altos', 'East Foothills']

	if city == "Oakland":
		return oakland
	if city == "San Francisco":
		return san_francisco
	if city == "Daly City":
		return daly_city
	if city == "South San Francisco":
		return south_san_francisco
	if city == "Pacifica":
		return pacifica
	if city == "San Bruno":
		return san_bruno
	if city == "Millbrae" or city == "Hillsborough" or city == "Burlingame":
		return millbrae
	if city == "Foster City" or city == "Highlands-Baywood Park" or city == "San Mateo":
		return san_mateo
	if city == "Belmont" or city == "San Carlos" or city == "Emerald Hills" or city == "North Fair Oaks" or city == "Woodside" or city == "Atherton" or city == "Redwood City":
		return redwood_city

	if city == "Palo Alto" or city == "Menlo Park" or city == "Portola Valley" or city == "West Menlo Park" or city == "Stanford":
		return between_redwood_and_mountainview
	if city == "Mountain View" or city == "Los Altos" or city == "Sunnyvale" or city == "Loyola" or city == "Cupertino":
		return mountainview
	if city == "San Jose" or city == "Santa Clara" or city == "Campbell" or city == "Cupertino" or city == "Milpitas" or city == "Cambrian Park" or city == "East Foothills":
		return san_jose
	else:
		return []





def update_user_list(logged_in_user):
	user_gamification = Gamification.objects.get(user=logged_in_user)
	user_list = user_gamification.discover_list
	try:
		last_user_id = user_list.latest('id').id
	except: 
		return 
	new_users = User.objects.filter(is_active=True).filter(id__gte=last_user_id)
	current_location = Address.objects.get(user=logged_in_user)
	current_state = current_location.state
	current_city = current_location.city
	new_close_users = new_users.filter(address__state=current_state).filter(address__city=current_city)
	if current_state == 'California':
		close_cities = find_close_cities(current_city)
	if close_cities:
		new_close_users = new_users.filter(address__state=current_state).filter(address__city__in=close_cities)
	else:
		new_close_users = new_users.filter(address__state=current_state).filter(address__city=current_city)
	#user_gamification.discover_list.add(*new_close_users)
	#user_gamification.save()
	'''
	new_close_users = list(new_users.filter(address__state=current_state).filter(address__city=current_city))
	excluded_users = []
	matches = Match.objects.filter(
	Q(user1=logged_in_user, user1_approved=True) | Q(user2=logged_in_user, user2_approved=True)
	)
	for match in matches:
	if match.user1 != logged_in_user:
	excluded_users.append(match.user1)
	else:
	excluded_users.append(match.user2)
	'''
	#new_users = [x for x in new_close_users if x not in excluded_users]
	user_gamification.discover_list.add(*new_close_users)
	user_gamification.save()


def pop_user(logged_in_user, single_user):
	user_gamification = Gamification.objects.get(user=logged_in_user)
	user_list = user_gamification.discover_list
	user_list.remove(single_user)
	user_gamification.save()




def reset_discover(request):
	request.session['%s' % request.user.username]=request.user.username	
	users_all = User.objects.filter(is_active=True)
	num_of_users = users_all.count() + 1
	ran_num = randint(0, num_of_users - 20)
	users_all = list(User.objects.filter(is_active=True)[ran_num:ran_num+20])
	cache.set('cache_for_%s' % request.session['%s' % request.user.username], users_all, 120)
	#return HttpResponseRedirect(reverse('discover'))
	return redirect('http://www.frenvu.com/discover/?page=1')


#def find_somewhat_close_users(request):



#def check_if_already_friends(user1, user2):



'''
The Discover function creates functionality similar to tinder. Users can swipe or use arrow keys or press 
arrows through multiple users. We display their match percentage and all other functionality displayed
on the single user page.
'''


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def discover(request):
	

	try: 
		user_gamification = Gamification.objects.get(user=request.user)
	except:
		user_gamification = Gamification.objects.create(user=request.user)
	
	page = request.GET.get('page')
	page_int = int(page)

	info = Info.objects.get(user=request.user)

	if page_int == 1 and info.new_to_discover == False:
		update_user_list(request.user)

	
	if info.new_to_discover == True:
		create_user_list(request.user)
		info.new_to_discover = False
		info.save()

	if user_gamification.discover_list.count() == 0:
		no_users = True
		return render_to_response('profiles/discover.html', locals(), context_instance=RequestContext(request))
		#return HttpResponseRedirect(reverse('home'))
	else:
		no_users = False

	user_list = list(user_gamification.discover_list.all())
	paginator = Paginator(user_list, 1)
	

	if user_gamification.discover_list.count() == 0:
		no_users = True
		return render_to_response('profiles/discover.html', locals(), context_instance=RequestContext(request))
		#return HttpResponseRedirect(reverse('home'))
	else:
		no_users = False

	try:
		if page != False:
			users = paginator.page(page)
			single_user = users.object_list[0]

			try: 
				match = Match.objects.get(user1=request.user, user2=single_user)
			except: 
				match, created = Match.objects.get_or_create(user1=single_user, user2=request.user)
			#test to see if friend, and if they are friends, skip
			'''
			if (match.user1_approved == True and match.user2_approved == True):
			page_int = int(page)
			new_page = page_int + 1
			new_page_u = unicode(new_page)
			users = paginator.page(new_page_u)
			single_user = users.object_list[0]
			'''
			#if single user is self, skip
			if single_user == request.user:
				page_int = int(page)
				new_page = page_int + 1
				new_page_u = unicode(new_page)
				users = paginator.page(new_page_u)
				single_user = users.object_list[0]

			try:
				match.distance = round(calc_distance(request.user, single_user))
			except:
				# they have an invalid location
				match.distance = 10000000

			info = Info.objects.get(user=request.user)
			is_new_user = info.is_new_user
			if is_new_user:
				pass
			else:	
				match.percent = match_percentage(match.user1, match.user2)
				if match.percent == 0:
					single_user_new = True
			try:
				su_info = Info.objects.get(user=single_user)
				if su_info.is_new_user == True:
					single_user_new = True
			except: 
				single_user_new = False
			match.save()
			try:
				profile_pic = UserPicture.objects.get(user=user, is_profile_pic=True)
			except: 
				pass
			interests = find_same_interests(request.user, single_user)
			pop_user(request.user, single_user)



	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		users = paginator.page(1)

	except EmptyPage:
		#If page is out of range, deliver last page of results
		users = paginator.page(paginator.num_pages)


	return render_to_response('profiles/discover.html', locals(), context_instance=RequestContext(request))




@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def friends(request):
	matches = Match.objects.filter(
		Q(user1=request.user) | Q(user2=request.user)
		).filter(are_friends=True)
	number_of_friends = matches.count()
	return render_to_response('profiles/friends.html', locals(), context_instance=RequestContext(request))




#Shows all pictures that the logged in user has 
@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def all_pictures(request): 
	try: 
		pictures = UserPicture.objects.filter(user=request.user)
		num_of_pics = pictures.count()
		for pic in pictures.all():
			print pic
	except: 
		num_of_pics = 0
	return render_to_response('profiles/pictures.html', locals(), context_instance=RequestContext(request))




def delete_picture(request, pic_id):
	picture = UserPicture.objects.get(pk=pic_id)
	picture.delete()
	delete_s3_pic(user, picture)
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
				print new_form.city
				print new_form.state
				if check_valid_location(new_form.city, new_form.state) == False:
					messages.success(request, "We're sorry but you didn't enter a valid location")
					return HttpResponseRedirect('/edit/')
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
		gender = request.POST['gender_form']
		
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


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def edit_profile(request):
	user = request.user
	pictures = UserPicture.objects.filter(user=user)
	num_of_pictures = UserPicture.objects.filter(user=user).count()
	addresses = Address.objects.filter(user=user)
	jobs = Job.objects.filter(user=user)
	info = Info.objects.get(user=user)
	gender = info.gender
	if gender == 'Male':
		is_male = True
	else:
		is_female = True
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
	email = str(request.POST['email'])
	password = str(request.POST['password'])


	try: 
		user1 = User.objects.get(email=email)
	except: 
		messages.error(request, "Please double check your username or email address and password")
		return HttpResponseRedirect(reverse('home'))
	username = user1.username
	user = authenticate(username=username, password=password)
	logged_in_user = User.objects.get(email=email)

	if user is not None:
		# if user deactivated their account and logged in, they are no longer deactivated
		if user.is_active == False:
			

			logged_in_user.save()
			if not DEBUG: 
				email = request.user.email
				subject = 'A user is reactivating their account.'
				message = '%s wants to reactivate their account.' % (username,)
				msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
				msg.content_subtype = "html"
				msg.send()
			messages.success(request, "We missed you!")
		login(request, user)
		return HttpResponseRedirect(reverse('home'))
	else:
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

	email = str(request.POST['email'])

	if '@' not in email:
		messages.success(request, 'Please provide a valid email address')
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))

	email2 = email.split('@')[0]
	email_as_username = email2.translate(None, " '?.!/;:@#$%^&(),[]{}`~-_=+*|<>")
	if len(email_as_username) == 0:
		messages.error("Please provide a valid email")
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))
	password = request.POST['password']
	confirm_password = request.POST['repassword']



	if email and password:
			if password == confirm_password:
				try:
					new_user = User.objects.get(email=email)
					messages.error(request, "Sorry but this email is already associated with an account")
					return render_to_response('home.html', locals(), context_instance=RequestContext(request))
				except:	
					pass

				new_user = User.objects.create(username=email_as_username, password=password)
				new_user.set_password(password)
				new_user.email = email
				
				new_user.save()
				new_user = authenticate(username=email_as_username, password=password)
				login(request, new_user)
				return HttpResponseRedirect(reverse('new_user_info'))
			else:
				messages.error(request, "Please make sure both passwords match")
	return render_to_response('home.html', locals(), context_instance=RequestContext(request))




#Displays the profile page of a specific user and their match % against the logged in user

def single_user(request, username):
	if request.user.is_authenticated():
	
		try:
			user = User.objects.get(username=username)
			if user.is_active:
				single_user = user
		except:
			raise Http404
		try:
			profile_pic = UserPicture.objects.get(user=single_user, is_profile_pic=True)
		except: 
			pass
		 
		try:
			info = Info.objects.get(user=single_user)
		except:
			pass
		try:
			job = Job.objects.get(user=single_user)
		except:
			pass
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


			try:
				su_info = Info.objects.get(user=single_user)
				single_user_is_new = su_info.is_new_user
			except: 
				single_user_is_new = False
			if (match.user1 == single_user and match.user1_approved == True and match.user2_approved == False) or (match.user2 == single_user and match.user2_approved == True and match.user1_approved == False):
				respond_to_request = True
			interests = find_same_interests(request.user, single_user)



		
		messages_in_inbox = DirectMessage.objects.filter(receiver=request.user)
		direct_messages = DirectMessage.objects.get_num_unread_messages(request.user)
		request.session['num_of_messages'] = direct_messages
		return render_to_response('profiles/single_user.html', locals(), context_instance=RequestContext(request))
	else:
		try:
			user = User.objects.get(username=username)
			if user.is_active:
				single_user = user
		except:
			raise Http404
		try:
			profile_pic = UserPicture.objects.get(user=single_user, is_profile_pic=True)
		except: 
			pass
		try:
			info = Info.objects.get(user=single_user)
		except:
			pass
		try:
			job = Job.objects.get(user=single_user)
		except:
			pass
		return render_to_response('profiles/single_user_logged_out.html', locals(), context_instance=RequestContext(request))	


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def single_user_pictures(request, username):
	pictures = UserPicture.objects.filter(user__username=username)
	num_of_pics = pictures.count()
	return render_to_response('profiles/single_user_pictures.html', locals(), context_instance=RequestContext(request))


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
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

def about(request): 
	return render_to_response('home/about.html', locals(), context_instance=RequestContext(request))

def contact(request): 
	return render_to_response('home/contact.html', locals(), context_instance=RequestContext(request))

def cookies(request): 
	return render_to_response('home/cookies.html', locals(), context_instance=RequestContext(request))

def help(request): 
	return render_to_response('home/help.html', locals(), context_instance=RequestContext(request))

def jobs(request): 
	return render_to_response('home/jobs.html', locals(), context_instance=RequestContext(request))

def find_friends(request): 
	return render_to_response('home/find_friends.html', locals(), context_instance=RequestContext(request))

def make_friends(request): 
	return render_to_response('home/make_friends.html', locals(), context_instance=RequestContext(request))

def make_friends_online(request): 
	return render_to_response('home/make_friends_online.html', locals(), context_instance=RequestContext(request))

def meet_people(request): 
	return render_to_response('home/meet_people.html', locals(), context_instance=RequestContext(request))

def meet_people_online(request): 
	return render_to_response('home/meet_people_online.html', locals(), context_instance=RequestContext(request))


@xframe_options_exempt
def press(request): 
	return render_to_response('press.html', locals(), context_instance=RequestContext(request))


def delete_picture(request, pic_id):
	user = request.user
	pic = UserPicture.objects.filter(user=user).get(id=pic_id)
	delete_s3_pic(request.user, pic)
	pic.delete()
	return HttpResponseRedirect(reverse('pictures'))


def delete_account(request):
	username = request.user.username
	deactivated_user = User.objects.get(username=username)
	deactivated_user.is_active = False
	deactivated_user.save()
	logout(request)
	messages.success(request, "Your account has been deactivated. Your account will be deleted in 30 days.")
	messages.success(request, "We're sorry to see you go, but if you change your mind before then, just log back in to reactivate it!")
	if not CURRENTLY_LOCALLY_TESTING: 
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


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def new_picture(request):
	if request.method == 'POST':
		num_of_pics = UserPicture.objects.filter(user=request.user).count()
		next_pic = str(num_of_pics + 1)
		pic_form = UserPictureForm(request.POST, request.FILES)
		if pic_form.is_valid():
			form = pic_form.save(commit=False)
			image = pic_form.cleaned_data["image"]
			if image:
				if "profile_pic" in request.POST:
					form.is_profile_pic = True
				form.user = request.user
				form.image.save("%s_pic-%s.jpg" % (request.user.username, next_pic), image)
				#form.save()
	return HttpResponseRedirect(reverse('pictures'))



@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def make_profile_pic(request, pic_id):
	pic = UserPicture.objects.get(id=pic_id)
	pic.is_profile_pic = True
	pic.save()
	return HttpResponseRedirect(reverse('pictures'))





@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def ice_breaker(request): 
	user1 = request.user
	user1_interests = UserInterestAnswer.objects.filter(user=user1)
	if user1_interests.count() == 0:
		messages.success(request, "We're sorry, but you need to like a few interests first!")
		return HttpResponseRedirect(reverse('home'))

	user_interests = list(Interest.objects.filter(userinterestanswer__user=request.user))
	users_with_same_interests = User.objects.filter(userinterestanswer__interest__in=user_interests).exclude(userinterestanswer__user=request.user)
	if users_with_same_interests.count() == 0:
		messages.success(request, "We're sorry, but no one likes your interests")
		return HttpResponseRedirect(reverse('home'))
	random_user = random.choice(users_with_same_interests)
	random_user_interests = Interest.objects.filter(userinterestanswer__user=random_user)
	common_interests = []
	for interest in user_interests:
		if interest in random_user_interests:
			common_interests.append(interest)
	random_interest = random.choice(common_interests)
	try: 
		match = Match.objects.get(user1=request.user, user2=random_user)
		user1 = request.user
		user2 = random_user
	except:
		match, created = Match.objects.get_or_create(user1=random_user, user2=request.user)
		user1 = random_user
		user2 = request.user
	if match.user1 == request.user:
		match.currently_in_icebreaker_user1 = True
	else:
		match.currently_in_icebreaker_user2 = True

	if not CURRENTLY_LOCALLY_TESTING: 
		sender1 = User.objects.get(username="TeamFrenvu")
		sender2 = User.objects.get(username="TeamFrenvu")
	else:
		sender1 = user1
		sender2 = user2
	subject = "You two have an interest in common!"
	body_for_user1 = "You and %s both like %s! What exactly is it about %s that you like so much? Let %s know your thoughts because you can message each other for the next 3 hours! " %(user2.username, random_interest, random_interest, user2.username)
	body_for_user2 = "You and %s both like %s! What exactly is it about %s that you like so much? Let %s know your thoughts because you can message each other for the next 3 hours! " %(user1.username, random_interest, random_interest, user1.username)
	user1_message = DirectMessage.objects.create(subject=subject, body=body_for_user1, receiver=user1, sender=sender1)
	user2_message = DirectMessage.objects.create(subject=subject, body=body_for_user2, receiver=user2, sender=sender2)
	user1_message.sent = datetime.now()
	user2_message.sent = datetime.now()
	match.save()
	user1_message.save()
	user2_message.save()
	user_gamification = Gamification.objects.get(user=request.user)
	user_gamification.icebreaker_until_reset = datetime.now() + timedelta(hours=3)
	user_gamification.save()
	messages.success(request, "Please check your inbox, we've found a user that you have an interest in common with!")
	return HttpResponseRedirect(reverse('home'))

