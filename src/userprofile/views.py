from django.shortcuts import render, render_to_response,redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf

from .forms import CreateUserForm


#from .forms import CreateUserForm

def registration(request):
	#form = UserProfileForm()
	return render_to_response("registration.html")

def signup(request):
	user_form = CreateUserForm(data=request.POST)
	if request.method == 'POST':
		if user_form.is_valid():
			username = user_form.clean_username()
			password = user_form.clean_password2()
			user_form.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('/')
		else: 
			return redirect('/')
	return render_to_response('registration.html', context_instance=RequestContext(request))
