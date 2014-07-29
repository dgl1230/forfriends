# -*- coding: utf-8 -*-
import operator 
import datetime
#from datetime import date
#from datetime import *
import datetime
from random import randint

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, EmailMultiAlternatives

from forfriends.settings.deployment import EMAIL_HOST_USER, DEBUG
from forfriends.matching import match_percentage
from forfriends.distance import calc_distance
from matches.models import Match
from .models import Address, Job, Info, UserPicture
from .forms import AddressForm, InfoForm, JobForm, UserPictureForm
from interests.models import UserInterestAnswer
from visitors.models import Visitor
from directmessages.models import DirectMessage


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
		#users = User.objects.filter(is_active=True)
		#time1 = datetime.datetime.now()
		#number_of_users = User.objects.filter(is_active=True).count()
		#users_to_display = 0
		#random_user_ids = []
		#current_user_id = request.user.id
		#matches = []
		#users = []
		'''
		while users_to_display <= 9:
			random_user_id = randint(1, number_of_users)
			if random_user_id not in random_user_ids and random_user_id != current_user_id:
				try :
					user = User.objects.get(pk=id)
					users.append(user)
					random_user_ids.append(random_user_id)
					users_to_display += 1
				except:
					pass
		'''
		'''
		for user in users:	
			try: 
				match = Match.objects.get(user1=request.user, user2=user)
			except: 
				match, created = Match.objects.get_or_create(user1=user, user2=request.user)
			match.percent = match_percentage(request.user, user)
			try:
				match.distance = round(calc_distance(request.user, user))
			except:
				match.distance = 10000000
			match.save()	
			matches.append(match)
		'''
		'''
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
		'''		
		matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).order_by('-percent')
		#time2 = datetime.datetime.now()
		#time_difference = time2 - time1
		return render_to_response('all.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))

#Shows all pictures that the logged in user has 
def all_pictures(request): 
	pictures = UserPicture.objects.filter(user=request.user)
	return render_to_response('profiles/pictures.html', locals(), context_instance=RequestContext(request))


def delete_picture(request):
	pic_id = request.GET['picture_id']
	picture = UserPicture.objects.get(pk=pic_id)
	picture.delete()
	HttpResponseRedirect('/')



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

		user = request.user
		info = Info.objects.filter(user=user)
		InfoFormSet = modelformset_factory(Info, form=InfoForm, extra=0)
		formset_i = InfoFormSet(request.POST or None, queryset=info)

		if formset_i.is_valid():
			for form in formset_i:
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

	if info.exists():
		InfoFormSet = modelformset_factory(Info, form=InfoForm, extra=0)
		formset_i = InfoFormSet(request.POST or None, queryset=info)
	else:
		InfoFormSet = modelformset_factory(Info, form=InfoForm, extra=1)
		formset_i = InfoFormSet(request.POST or None, queryset=info)

	
	return render_to_response('profiles/edit_profile.html', locals(), context_instance=RequestContext(request))


#sorts the matches of user according to whatver the user specified 
def find_friends(request):
	number_of_users = User.objects.filter(is_active=True).count()
	index_start = randint(1, number_of_users - 5)
	index_end = index_start + 5
	print index_start
	print index_end

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
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
		else:
			messages.error(request, "Please double check your username and password")
	except: 
		messages.error(request, "Please double check your username and password")
	return render_to_response('home.html', locals(), context_instance=RequestContext(request))

def logout_user(request):
	logout(request)
	return render_to_response('home.html', locals(), context_instance=RequestContext(request))

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
	try:
		username = request.POST['username']
		password = request.POST['password']
		confirm_password = request.POST['repassword']
		email = request.POST['email']
		gender1 = request.POST['gender']
		day = request.POST['BirthDay']
		month = request.POST['BirthMonth']
		year = request.POST['BirthYear']
		datestr = str(year) + '-' + str(month) + '-' + str(day)
		birthday = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
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
			birthday = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
			user_age = calculate_age(birthday)

			if username and password and email:
				if password == confirm_password:
					new_user,created = User.objects.get_or_create(username=username, email=email)
					if created:
						new_user.set_password(password)
						new_info = Info(user=new_user)
						new_info.gender = gender
						new_info.birthday = birthday
						new_info.save()
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
			messages.error(request, "We're sorry but you must be at least 18 to signup!")
			return render_to_response('home.html', locals(), context_instance=RequestContext(request))
	except:
		messages.error(request, "Please fill out all fields")
	return render_to_response('home.html', locals(), context_instance=RequestContext(request))

#Displays the profile page of a specific user and their match % against the logged in user
def single_user(request, username):
	try:
		user = User.objects.get(username=username)
		if user.is_active:
			single_user = user
	except:
		raise Http404
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
	matches = Match.objects.filter(
			Q(user1=request.user) | Q(user2=request.user)
			).order_by('-percent')
	for match in matches: 
		match.percent = match_percentage(match.user1, match.user2)
		try:
			match.distance = round(calc_distance(request.user, u))
		except:
			match.distance = 10000000
		match.save()

	return render_to_response('profiles/find_friends.html', locals(), context_instance=RequestContext(request))	


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


def delete_account(request):
	username = request.user.username
	deleted_user = User.objects.get(username=username)
	logout(request)
	deleted_user.delete()
	messages.success(request, "Your account has been deleted. We'll miss you!")
	return render_to_response('home.html', locals(), context_instance=RequestContext(request))


def contact_us(request):
	if request.POST:
		message = request.POST['message']
		send_mail('Inquuiry', message , EMAIL_HOST_USER, [EMAIL_HOST_USER])
	return render_to_response ('contact_us.html', locals(), context_instance=RequestContext(request))







