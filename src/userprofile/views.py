from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login

from .forms import CreateUserForm


def registration(request):
	return render_to_response("profile_home.html")

def signup(request):
	if request.method == 'POST':
		user_form = CreateUserForm(data=request.POST)
		print "userform created"
		if user_form.is_valid():
			print "it's valid"
			username = request.POST['username']
			password = user_form.clean_password2()
			user_form.save()
			#user = authenticate(username=username, password=password)
			#login(request, user)
			return HttpResponseRedirect('/')
		else: 
			print "it's not valid"
			print user_form.errors
			return HttpResponseRedirect('/')
	else:
		form  = CreateUserForm
		return render_to_response('registration.html', {'form': form},  
		 context_instance=RequestContext(request))