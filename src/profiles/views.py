import operator 

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.db.models import Q

from forfriends.matching import match_percentage
from matches.models import Match
from .models import Address, Job, Info, UserPicture
from .forms import AddressForm, InfoForm, JobForm, UserPictureForm
from interests.models import UserInterestAnswer




'''The view for the home page of a user. If they're logged in, it shows relevant
matches for them, otherwise it shows the home page for non-logged in viewers '''
def all(request):
	if request.user.is_authenticated():
		users = User.objects.filter(is_active=True)
		try: 
			matches = Match.objects.filter(user=request.user)
			for match in matches: 
				try: 
					match.percent = match_percentage(request.user, match.matched)
				except:
					match.percent = 0
				match_num = match.percent 
				match.percent = match_num
				match.save()
		except Exception:
			pass
		return render_to_response('all.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))

#Shows all pictures that the logged in user has 
def all_pictures(request): 
	user = request.user
	return render_to_response('pictures.html', locals(), context_instance=RequestContext(request))



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
				#new_form.user = request.user
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
				#new_form.user = request.user
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
	picture = UserPicture.objects.get(user=user)
	addresses = Address.objects.filter(user=user)
	jobs = Job.objects.filter(user=user)
	info = Info.objects.filter(user=user)

	user_picture_form = UserPictureForm(request.POST or None, request.FILES or None, prefix='pic', instance=picture)

	AddressFormSet = modelformset_factory(Address, form=AddressForm, extra=0)
	formset_a = AddressFormSet(queryset=addresses)

	JobFormSet = modelformset_factory(Job, form=JobForm, extra=0)
	formset_j = JobFormSet(queryset=jobs)

	InfoFormSet = modelformset_factory(Info, form=InfoForm, extra=0)
	formset_i = InfoFormSet(request.POST or None, queryset=info)

	if user_picture_form.is_valid():
		form3 = user_picture_form.save(commit=False)
		form3.save()
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



#Displays the profile page of a specific user and their match % against the logged in user
def single_user(request, username):
	try:
		user = User.objects.get(username=username)
		if user.is_active:
			single_user = user
	except:
		raise Http404
	set_match, created = Match.objects.get_or_create(user=request.user, matched=single_user)
	try:
		set_match.percent = match_percentage(request.user, single_user)
	except: 
		print "failed"
		set_match.percent = 0
	set_match.good_match = Match.objects.good_match(request.user, single_user)
	set_match.save()
	match = set_match.percent 
	interests = UserInterestAnswer.objects.filter(user=single_user)
	return render_to_response('single_user.html', locals(), context_instance=RequestContext(request))	


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



