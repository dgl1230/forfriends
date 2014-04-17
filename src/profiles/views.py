from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

#from interests.matching import points, match_percentage
#from matches.models import Match, JobMatch
from .models import Address, Job, Info, UserPicture
from .forms import AddressForm, InfoForm, JobForm, UserPictureForm


def all(request):
	if request.user.is_authenticated():
		users = User.objects.filter(is_active=True)
		try: 
			matches = Match.objects.user_matches(request.user)
		except Exception:
			pass
		return render_to_response('all.html', locals(), context_instance=RequestContext(request))
	else:
		return render_to_response('home.html', locals(), context_instance=RequestContext(request))


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


def single_user(request, username):
	try:
		user = User.objects.get(username=username)
		if user.is_active:
			single_user = user
	except:
		raise Http404
	return render_to_response('single_user.html', locals(), context_instance=RequestContext(request))	