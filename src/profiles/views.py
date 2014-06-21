# -*- coding: utf-8 -*-
import operator 
import datetime
from datetime import date

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from forfriends.matching import match_percentage
from matches.models import Match
from .models import Address, Job, Info, UserPicture
from .forms import AddressForm, InfoForm, JobForm, UserPictureForm
from interests.models import UserInterestAnswer
from visitors.models import Visitor


'''Implements the 'add friend' button when viewing a user's profile
If both users click this button on each other's profile, they can message'''
def add_friend(request, username):
	user_match, created = Match.objects.get_or_create(user=request.user, matched__username=username)
	visited_user = User.objects.get(username=username)
	visited_match, created = Match.objects.get_or_create(user=visited_user, matched=request.user)
	user_match.approved = True
	user_match.user = request.user 
	user_match.save()
	if (user_match.approved == True and visited_match.approved == True):
		messages.success(request, "%s also is interested in being your friend - You can now message each other!" %username)
	else:
		messages.success(request, "%s has received your request. If %s is interested too, they will add you!" %(username, username))
	return HttpResponseRedirect('/')


'''The view for the home page of a user. If they're logged in, it shows relevant
matches for them, otherwise it shows the home page for non-logged in viewers '''
def all(request):
	if request.user.is_authenticated(): 
		users = User.objects.filter(is_active=True)
		for u in users:
			if u != request.user:
				match, created = Match.objects.get_or_create(user=request.user, matched=u)
				match.percent = match_percentage(request.user, u)
				match.save()
		matches = Match.objects.filter(user=request.user).order_by('-percent')
		return render_to_response('all.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))

#Shows all pictures that the logged in user has 
def all_pictures(request): 
	pictures = UserPicture.objects.filter(user=request.user)
	return render_to_response('profiles/pictures.html', locals(), context_instance=RequestContext(request))



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
			messages.success(request, 'Profile details updated.')
		else:
			messages.error(request, 'Profile details did not update.')
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
		PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=0)
		formset_p = PictureFormSet(request.POST or None, request.FILES, queryset=pictures)

		if formset_p.is_valid():
			for form in formset_p:
				new_form = form.save(commit=False)
				new_form.user = user
				new_form.save()
			messages.success(request, 'Profile details updated.')
		else:
			messages.error(request, 'Profile details did not update.')
		#return render_to_response('profiles/edit_address.html', locals(), context_instance=RequestContext(request))
		return HttpResponseRedirect('/edit/')
	else:
		raise Http404


def edit_profile(request):
	user = request.user
	pictures = UserPicture.objects.filter(user=user)
	addresses = Address.objects.filter(user=user)
	jobs = Job.objects.filter(user=user)
	info = Info.objects.filter(user=user)

	if pictures.exists():
		PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=0)
		formset_p = PictureFormSet(queryset=pictures)
	else:
		PictureFormSet = modelformset_factory(UserPicture, form=UserPictureForm, extra=1)
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
	matches = Match.objects.filter(user=request.user)
	for match in matches: 
				try: 
					match.percent = match_percentage(request.user, match.matched)
				except:
					match.percent = 0
				match_num = match.percent 
				match.percent = match_num
				match.save()
	matches = matches.order_by('-percent')
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
		set_match, created = Match.objects.get_or_create(user=request.user, matched=single_user)
		try:
			set_match.percent = match_percentage(request.user, single_user)
		except: 
			print "failed"
			set_match.percent = 0
		visited_list, created = Visitor.objects.get_or_create(main_user=single_user)
		visited_list.visitors.add(request.user)
		visited_list.save()
		
		set_match.save()
		match = set_match.percent 
	
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


#Show all the visitors that have viewed the logged in user's profile page
def all_visitors(request): 
	visitors1, created = Visitor.objects.get_or_create(main_user=request.user)
	visitors = [val for val in visitors1.visitors.all()]
	return render_to_response('profiles/visitors.html', locals(), context_instance=RequestContext(request))


def terms_and_agreement(request): 
	return render_to_response('terms.html', locals(), context_instance=RequestContext(request))






