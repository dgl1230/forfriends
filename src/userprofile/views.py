from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.contrib.auth.decorators import login_required


from .forms import CreateUserForm, AuthenticateForm, InterestForm


@login_required
def add_interest(request):
	if request.method == 'POST':
		form = InterestForm(data=request.POST)
		if form.is_valid:
			interest = form.save(commit=False)
			interest.user = request.user
			interest.save()
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')


def home(request):
	return render_to_response('profile_home.html', context_instance=RequestContext(request))

def login_view(request):
	if request.method == 'POST':
		form = AuthenticateForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())

			return HttpResponseRedirect('profile_home')
		else: 
			return HttpResponseRedirect('/')
	else: 
		return HttpResponseRedirect('/')


def signup(request):
	if request.method == 'POST':
		form = CreateUserForm(data=request.POST)
		if form.is_valid():
			print "it's no valid"
			birthday = request.POST['birthday']
			gender = request.POST['gender']
			username = form.clean_username()
			password = form.clean_password2()
			form.save()
			user = authenticate(username=username, password=password)
			new_profile = UserProfile(user=user)
			new_profile.birthday = birthday
			new_profile.gender = gender
			new_profile.save()
			print "profile saved"
			login(request, user)
			return HttpResponseRedirect('profile_home')
		else: 
			print "it's not valid"
	form  = CreateUserForm
	return render_to_response('registration.html', {'form': form},  
		context_instance=RequestContext(request))

