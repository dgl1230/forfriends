# -*- coding: utf-8 -*-
import operator 
import datetime
from datetime import date, datetime, timedelta
#from datetime import *

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


from forfriends.settings.deployment import EMAIL_HOST_USER, DEBUG, MEDIA_URL
from forfriends.matching import match_percentage
from forfriends.distance import calc_distance
from matches.models import Match
from .models import Address, Job, Info, UserPicture, Gamification
from .forms import AddressForm, InfoForm, JobForm, UserPictureForm, JcropForm
from interests.models import UserInterestAnswer, Interest
from visitors.models import Visitor
from directmessages.models import DirectMessage
from questions.models import Question, UserAnswer


'''Implements the 'add friend' button when viewing a user's profile
If both users click this button on each other's profile, they can message'''
def add_friend(request, username):
	try: 
		match = Match.objects.get(user1=request.user, user2__username=username)
		match.user1_approved = True
	except: 
		match = Match.objects.get(user1__username=username, user2=request.user)
		match.user2_approved = True
	if (match.user1_approved == True and match.user2_approved == True):
		user1 = match.user1
		user2 = match.user2
		subject = "You have a new friend!"
		body_for_user1 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user2.username)
		body_for_user2 = "Congrats! You and %s both requested to be each other's friends, so now you can message each other!" %(user1.username)
		user1_message = DirectMessage.objects.create(subject=subject, body=body_for_user1, receiver=user1)
		user2_message = DirectMessage.objects.create(subject=subject, body=body_for_user2, receiver=user2)
		user1_message.sent = datetime.datetime.now()
		user2_message.sent = datetime.datetime.now()
		user1_message.save()
		user2_message.save()
		messages.success(request, "%s also is interested in being your friend - You can now message each other!" %username)
	else:
		messages.success(request, "%s has received your request. If %s is interested too, they will add you!" %(username, username))
	single_user = User.objects.get(username=username)
	match.save()
	return render_to_response('profiles/single_user.html', locals(), context_instance=RequestContext(request))


'''The view for the home page of a user. If they're logged in, it shows relevant
matches for them, otherwise it shows the home page for non-logged in viewers '''
def all(request):
	if request.user.is_authenticated(): 
		try: 
			info = Info.objects.get(user=request.user)
			assert(info.is_new_user == False)
		except: 
			return HttpResponseRedirect(reverse('handle_new_user'))
		try:
			#time1 = datetime.datetime.now()
			user_gamification = Gamification.objects.get(user=request.user)
			circle = user_gamification.circle.all()
			circle_num = 0
			for match in circle: 
				circle_num += 1
			if circle <= 6:
				generate_circle(request.user)
				user_gamification = Gamification.objects.get(user=request.user)
			return render_to_response('all.html', locals(), context_instance=RequestContext(request))
		except: 
			#the user has never calcuated their circle
			user_gamification = Gamification.objects.create(user=request.user)
			user_gamification.save()
			generate_circle(request.user)
			#makes it so that the circle is displayed right away instead of having to click "generate circle"
			user_gamification = Gamification.objects.get(user=request.user)
			return render_to_response('all.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))


def generate_circle(logged_in_user):
	if logged_in_user.is_authenticated(): 
			try: 
				assert (circle_distance(logged_in_user) == 1)
				return
			except: 
				#either a new user or someone who hasn't used the site much
				num_10m = 0
				num_20m = 0
				num_30m = 1
				num_40m = 0
				num_50m = 0 
				users = User.objects.filter(is_active=True)
				for user in users: 
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
					matches = Match.objects.filter(
						Q(user1=logged_in_user) | Q(user2=logged_in_user)
					).order_by('-percent')[:7]
					user_gamification = Gamification.objects.get(user=logged_in_user)
					for match in matches: 
						user_gamification.circle.add(match) 
					user_gamification.circle_reset_started = datetime.now()
					user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
					user_gamification.save()


def circle_distance(logged_in_user):
	matches_basic = Match.objects.filter(
			Q(user1=logged_in_user) | Q(user2=logged_in_user)
			)
	matches_10m = matches_basic.filter(is_10_miles=True)
	if matches_10m.count() >= 10: 
		matches = matches_10m.order_by('-percent')[:7]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	matches_20m = matches_basic.filter(is_20_miles=True)
	if matches_20m.count() >= 10:
		matches = matches_20m.order_by('-percent')[:7]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	matches_30m = matches_basic.filter(is_30_miles=True)
	if matches_30m.count() >= 10:
		matches = matches_30m.order_by('-percent')[:7]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	matches_40m = matches_basic.filter(is_40_miles=True)
	if matches_40m.count() >= 10:
		matches = matches_40m.order_by('-percent')[:7]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	matches_50m = matches_basic.filter(is_50_miles=True)
	if matches_50m.count() >= 10:
		matches = match_50m.order_by('-percent')[:7]
		user_gamification = Gamification.objects.get(user=logged_in_user)
		for match in matches: 
			user_gamification.circle.add(match) 
		user_gamification.circle_reset_started = datetime.now()
		user_gamification.circle_time_until_reset = datetime.now() + timedelta(hours=24)
		user_gamification.save()
		return 1
	else:
		return 0 




def handle_new_user(request):
	try:
		info = Info.models.get(user=request.user)
		user_interests = UserInterestAnswer.objects.filter(user=request.user)
		user_questions = UserAnswer.objects.filter(user=request.user)
	except: 
		user_interests = 0
		user_questions = 0
	try: 
		#if we get an error, then this means they signed up with google or facebook
		# so we need to get more info from them first 
		address = Address.objects.get(user=request.user)
		assert(info.signed_up_with_fb_or_goog == False)
	except: 
		return HttpResponseRedirect(reverse('new_user_info'))
	if user_interests.count() < 10:
		return HttpResponseRedirect(reverse('new_user_interests'))
	if user_questions.count() < 10: 
		return HttpResponseRedirect(reverse('new_user_questions'))
	else: 
		info = Info.objects.get(user=request.user)
		info.is_new_user = False
		info.save()
		return HttpResponseRedirect(reverse('home'))


def new_user_info(request):
	if request.POST:
		name = request.POST['name']
		full_name = name.split()
		first_name = full_name[0]
		if len(full_name) == 2:
			last_name = full_name[1]
		elif len(full_name) >= 3:
			not_first_name = full_name[2:len(full_name)]
			last_name = full_name[1]
			for name in not_first_name:
				last_name = last_name + " " + name
		else: 
			first_name = full_name
		username = request.POST['username']
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
			if created:
				new_user.set_password(password)
				new_user.first_name = first_name
				if len(full_name) >= 2:
					new_user.last_name = last_name
				new_info = Info(user=request.user)
				new_address = Address(user=request.user)
				new_address.country = country
				new_address.state = state
				new_address.city = city
				new_info.gender = gender
				new_info.birthday = birthday
				new_info.signed_up_with_fb_or_goog = False
				new_info.save()
				new_address.save()
				new_user.save()
				if not DEBUG:
					subject = 'Thanks for registering with Frenvu!'
					line1 = 'Hi %s, \nThanks for making an account with Frenvu! My name is Denis, ' % (username,)
					html_line1 = 'Hi %s, \n<br>Thanks for making an account with Frenvu! My name is Denis, ' % (username,)

					line2 = "and I'm one of the Co-Founders of Frenvu. We're trying to make Frenvu a great"
					line3 = "place for fostering new friendships, but we're still an early company, so if "
					line4 = "you have any questions or concerns about the site, please feel free to reach "
					line5 = "out to me. I'd love to hear feedback from you or help you with any problem you're having! "

					line6 = "We hope you enjoy the site!\nSincerely,\nDenis and the rest of the team at Frenvu"
					html_line6 = "We hope you enjoy the site!\n<br>Sincerely,\n<br>Denis and the rest of the team at Frenvu"
					message = line1 + line2 + line3 + line4 + line5 + line6
					html_message = html_line1 + line2 + line3 + line4 + line5 + html_line6
					msg = EmailMultiAlternatives(subject, html_message, EMAIL_HOST_USER, [email])
					msg.content_subtype = "html"
					msg.send()
				return HttpResponseRedirect(reverse('handle_new_user'))
		else:
			messages.error(request, "We're sorry but you must be at least 18 to signup!")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('profiles/new_user.html', locals(), context_instance=RequestContext(request))



#def create_circle(user):



def random_user_page(request):
	max_user = User.objects.filter(is_active=True).latest('id').id
	while True: 
		try: 
			single_user = User.objects.get(pk=randint(1, max_user))
			break
		except:
			pass
	try: 
		match = Match.objects.get(user1=request.user, user2=single_user)
	except: 
		match, created = Match.objects.get_or_create(user1=single_user, user2=request.user)
	user1 = match.user1
	user2 = match.user2
	match.percent = match_percentage(user1, user2)
	try:
		match.distance = round(calc_distance(request.user, user))
		if match.distance <= 10:
			match.is_10_miles = True
			match.is_20_miles = True 
			match.is_30_miles = True
			match.is_40_miles = True
			match.is_50_miles = True
		elif match.distance <= 20:
			match.is_20_miles = True 
			match.is_30_miles = True
			match.is_40_miles = True
			match.is_50_miles = True
		elif match.distance <= 30:
			match.is_30_miles = True
			match.is_40_miles = True
			match.is_50_miles = True
		elif match.distance <= 40:
			match.is_40_miles = True
			match.is_50_miles = True
		elif match.distance <= 50:
			match.is_50_miles = True
	except:
		match.distance = 10000000
	match.save()
	return render_to_response('profiles/single_user.html', locals(), context_instance=RequestContext(request))	





#Shows all pictures that the logged in user has 
def all_pictures(request): 
	username = request.user.username
	user = User.objects.get(username=username)
	try: 
		pictures = UserPicture.objects.filter(user=user)
	except: 
		pass
	return render_to_response('profiles/pictures.html', locals(), context_instance=RequestContext(request))


def calculate_circle(request):
	user_gamification = Gamification.objects.get(user=request.user)
	if user_gamification.circle_reset_started and user_gamification.circle_time_until_reset:
		circle_reset_started = user_gamification.circle_reset_started
		circle_time_until_reset = user_gamification.circle_time_until_reset
		check_circle_time = (circle_time_until_reset - circle_reset_started).seconds / 60.0
		if check_circle_time >= 24: 
			generate_circle(request.user)
		else: 
			messages.error(request, "sorry, you need to wait!")
	return render_to_response('all.html', locals(), context_instance=RequestContext(request))



def delete_picture(request, pic_id):
	#pic_id = request.GET['picture_id']
	picture = UserPicture.objects.get(pk=pic_id)
	picture.delete()
	#HttpResponseRedirect('/')
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
			messages.success(request, 'Profile details did not update.')
		else:
			messages.error(request, 'Please fill out all fields.')
		#return render_to_response('profiles/edit_address.html', locals(), context_instance=RequestContext(request))
		return HttpResponseRedirect('/edit/')
	else:
		raise Http404


def edit_info(request):
	if request.method == 'POST':
		info = Info.objects.get(user=request.user)
		#InfoFormSet = modelformset_factory(Info, form=InfoForm, extra=0)
		#formset_i = InfoFormSet(request.POST or None, queryset=info)

		'''if formset_i.is_valid():
			for form in formset_i:
				new_form = form.save(commit=False)
				new_form.user = request.user
				new_form.save()
			messages.success(request, 'Profile details updated.')
		else:
			messages.error(request, 'Profile details did not update.')
		'''
		username = request.POST.get('username_form')
		first_name = request.POST.get('first_name_form')
		last_name = request.POST.get('last_name_form')
		bio = request.POST.get('bio_form')
		gender = request.POST.get('gender_form')
		request.user.username = username
		request.user.first_name = first_name
		request.user.last_name = last_name
		request.user.save()
		info.bio = bio
		info.gender = gender
		info.save()

		
		#return render_to_response('profiles/edit_address.html', locals(), context_instance=RequestContext(request))
		return HttpResponseRedirect('/edit/')
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
	info = Info.objects.filter(user=user)

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
		user = authenticate(username=username, password=password)
		if user is not None:
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
			return HttpResponseRedirect('/')
		else:
			messages.error(request, "Please double check your username and password")
	except: 
		messages.error(request, "Please double check your username and password")
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

#Creates a new user and assigns the appropriate fields to the user
def register_new_user(request):
	name = request.POST['name']
	full_name = name.split()
	first_name = full_name[0]
	if len(full_name) == 2:
		last_name = full_name[1]
	elif len(full_name) >= 3:
		not_first_name = full_name[2:len(full_name)]
		last_name = full_name[1]
		for name in not_first_name:
			last_name = last_name + " " + name
	else: 
		first_name = full_name

	username = request.POST['username']
	password = request.POST['password']
	confirm_password = request.POST['repassword']
	email = request.POST['email']
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
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))

	if user_age >= 18:
		datestr = str(year) + '-' + str(month) + '-' + str(day)
		birthday = datetime.strptime(datestr, '%Y-%m-%d').date()
		user_age = calculate_age(birthday)

		if username and password and email:
			if username != password: 
				if password == confirm_password:
					new_user,created = User.objects.get_or_create(username=username, email=email)
					if created:
						new_user.set_password(password)
						new_user.first_name = first_name
						if len(full_name) >= 2:
							new_user.last_name = last_name
						new_info = Info(user=new_user)
						new_address = Address(user=new_user)
						new_address.country = country
						new_address.state = state
						new_address.city = city
						new_info.gender = gender
						new_info.birthday = birthday
						new_info.save()
						new_address.save()
						new_user.save()
						new_user = authenticate(username=username, password=password)
						if not DEBUG:
							subject = 'Thanks for registering with Frenvu!'
							line1 = 'Hi %s, \nThanks for making an account with Frenvu! My name is Denis, ' % (username,)
							html_line1 = 'Hi %s, \n<br>Thanks for making an account with Frenvu! My name is Denis, ' % (username,)

							line2 = "and I'm one of the Co-Founders of Frenvu. We're trying to make Frenvu a great"
							line3 = "place for fostering new friendships, but we're still an early company, so if "
							line4 = "you have any questions or concerns about the site, please feel free to reach "
							line5 = "out to me. I'd love to hear feedback from you or help you with any problem you're having! "

							line6 = "We hope you enjoy the site!\nSincerely,\nDenis and the rest of the team at Frenvu"
							html_line6 = "We hope you enjoy the site!\n<br>Sincerely,\n<br>Denis and the rest of the team at Frenvu"
							message = line1 + line2 + line3 + line4 + line5 + line6
							html_message = html_line1 + line2 + line3 + line4 + line5 + html_line6
							msg = EmailMultiAlternatives(subject, html_message, EMAIL_HOST_USER, [email])
							msg.content_subtype = "html"
							msg.send()
						login(request, new_user)
						return HttpResponseRedirect('/')
					else:
						messages.error(request, "Sorry but this username is already taken")
				else:
					messages.error(request, "Please make sure both password match")
			else: 
				messages.error(request, "Pleasure make sure your username and password aren't the same!")
	else:
		messages.error(request, "We're sorry but you must be at least 18 to signup!")
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))
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
			visited_list, created = Visitor.objects.get_or_create(main_user=single_user)
			visited_list.visitors.add(request.user)
			visited_list.save()
	except: 
		raise Http404
	
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


def sort_by_match(request):

	matches1 = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			)
	for match in matches1: 
		#match.percent = match_percentage(match.user1, match.user2)
		try:
			match.distance = round(calc_distance(request.user, u))
		except:
			match.distance = 10000000
		match.save()
	matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).order_by('-percent')
	user_gamification = Gamification.objects.get(user=request.user)
	return render_to_response('all.html', locals(), context_instance=RequestContext(request))	
	


def sort_by_location(request):
	user_address = Address.objects.get(user=request.user)
	if user_address.city == False or user_address.state == False:
		messages.error(request, "You need to enter your location to use this feature")
		matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).order_by('?')
		return render_to_response('profiles/find_friends.html', locals(), context_instance=RequestContext(request))

	matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).order_by('-distance')
	for match in matches: 
		match.percent = match_percentage(match.user1, match.user2)
		try:
			match.distance = round(calc_distance(request.user, u))
		except:
			match.distance = 10000000
		match.save()
	return render_to_response('profiles/find_friends.html', locals(), context_instance=RequestContext(request))


#Show all the visitors that have viewed the logged in user's profile page
def all_visitors(request): 
	visitors1, created = Visitor.objects.get_or_create(main_user=request.user)
	visitors = [val for val in visitors1.visitors.all()]
	return render_to_response('profiles/visitors.html', locals(), context_instance=RequestContext(request))


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
	messages.success(request, "Your account has been deactivated. Your account will be deleleted in 30 days.")
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
		print 1
		pic_form = UserPictureForm(request.POST, request.FILES)
		print request.FILES
		print 2
		if pic_form.is_valid():
			print 3
			form = pic_form.save(commit=False)
			image = form.cleaned_data["preview"]
			if image:
				print 4
				form.user = user
				form.save()
	print pic_form.errors
	return HttpResponseRedirect(reverse('pictures'))


def new_picture1(request):
	# get the profile (i.e. the model containing the image to edit);
	# In this example, the model in question is the user profile model,
	# so we can use Django's get_profile() method.
	new_image = UserPicture.objects.create(user=request.user)
	#print len(request.FILES)
	#profile = request.user
	#image_upload_to = MEDIA_URL
  
	# define a fixed aspect ratio for the user image
	aspect = 105.0 / 75.0
	# the final size of the user image
  	
  	final_size = (105, 75) 
  	'''
  	x1 = request.POST.get("x1")
  	print "x1 is: ", x1
  	y1 = request.POST.get("y1")
  	print "y1 is: ", y1
  	x2 = request.POST.get("x2")
  	print "x2 is: ", x2
  	y2 = request.POST.get("y2")
  	print "y2 is: ", y2
  	w = request.POST.get("w")
  	print "w is: ", w
  	h = request.POST.get("h")
  	print "h is: ", h
  	cropped = request.POST.get("cropped")
  	print "cropped is: ", cropped
  	form = JcropForm(request.POST)
	if form.is_valid():
		# apply cropping
		form.crop()
		form.resize(final_size)
		form.save()
		# redirect to profile display page
		return HttpResponseRedirect("/")
	'''

  
	if request.method == "POST" and len(request.FILES) == 0:
		print "needs to be here"
		# user submitted form with crop coordinates
		form = JcropForm(request.POST)
		if form.is_valid():
			# apply cropping
			form.crop()
			form.resize(final_size)
			form.save()
			# redirect to profile display page
			return HttpResponseRedirect("/")
    
	elif request.method == "POST" and len(request.FILES):
		print "not cropping"
		# user uploaded a new image; save it and make sure it is not too large
		# for our layout
		img_fn = JcropForm.prepare_uploaded_img(request.FILES, new_image, (370, 500))
		if img_fn:
			# store new image in the member instance
			new_image.image = img_fn # 'avatar' is an ImageField
			try: 
				caption = request.POST['caption']
				new_image.caption = caption
			except: 
				pass
			new_image.save()
			# redisplay the form with the new image; this is the same as for
			# GET requests -> fall through to GET
      
	elif request.method != "GET":
		# only POST and GET, please
		return HttpResponse(status=400)
  
	# for GET requests, just display the form with current image
	form = JcropForm(initial        = { "imagefile": new_image.image },
					jcrop_options  = { 
										"aspectRatio":aspect,
										"setSelect": "[100, 100, 50, 50]",
									}
					)
	return HttpResponseRedirect(reverse('pictures'))



def ice_breaker(request): 
	user1 = request.user
	user1_interests = UserInterestAnswer.objects.filter(user=user1)
	max_interest = user1_interests.latest('id').id
	max_user = User.objects.latest('id').id
	while True: 
		try:
			random_interest = user1_interests.get(pk=randint(1, max_interest))
			assert (random_interest.importance_level == "Strongly Like" or random_interest.importance_level == "Like")
			break
		except: 
			pass
	while True: 
		try: 
			random_user = User.objects.get(pk=randint(1, max_user))
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
		match = Match.objects.get(user1=random_user, user2=request.user)
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
	messages.success(request, "Please check your inbox, we've found a user that you have an interest in common with!")
	return render_to_response('all.html', locals(), context_instance=RequestContext(request))








