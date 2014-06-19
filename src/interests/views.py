# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Interest, UserInterestAnswer, InterestPicture
from .forms import InterestForm


def create_interest(request):
	form = InterestForm(request.POST or None)
	if form.is_valid():
		interest = form.save(commit=False)
		interest.user = request.user
		interest.save()
		messages.success(request, 'Interest Created')
		return HttpResponseRedirect('/interests/')


	return render_to_response("interests/create.html", locals(),
		 context_instance=RequestContext(request))


def all_interests(request):
	interests_all = Interest.objects.exclude(userinterestanswer__user=request.user)
	paginator = Paginator(interests_all, 1)
	importance_levels = ['Strongly Like', 'Like', 'Neutral', 'Dislike', 'Strongly Dislike']

	page = request.GET.get('page')
	try:
		interests = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		interests = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		interets = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		interest_id = request.POST['interest_id']

		#user answer
		importance_level = request.POST['importance_level']

		user = User.objects.get(username=request.user)
		interest = Interest.objects.get(id=interest_id)
		try:
			interest_pic = InterestPicture.objects.get(interest=interest).filter(id=1)
		except: 
			pass

		#user answer save

		answered, created = UserInterestAnswer.objects.get_or_create(user=user, interest=interest)
		answered.importance_level = importance_level
		answered.save()

		messages.success(request, 'Answer Saved')
	return render_to_response('interests/all.html', locals(), context_instance=RequestContext(request))


def edit_interests(request):
	interests_all = Interest.objects.filter(userinterestanswer__user=request.user)
	paginator = Paginator(interests_all, 1)
	importance_levels = ['Strongly Like', 'Like', 'Neutral', 'Dislike', 'Strongly Dislike']

	page = request.GET.get('page')
	try:
		interests = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		interests = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		interets = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		interest_id = request.POST['interest_id']

		#user answer
		importance_level = request.POST['importance_level']

		user = User.objects.get(username=request.user)
		interest = Interest.objects.get(id=interest_id)
		try:
			interest_pic = InterestPicture.objects.get(interest=interest).filter(id=1)
		except: 
			pass

		#user answer save

		answered, created = UserInterestAnswer.objects.get_or_create(user=user, interest=interest)
		answered.importance_level = importance_level
		answered.save()

		messages.success(request, 'Changes Saved')
		return HttpResponseRedirect('')
	return render_to_response('interests/edit.html', locals(), context_instance=RequestContext(request))


# displays the interests for a particular user
def single_user_interests(request, username):
	interests_all = Interest.objects.filter(userinterestanswer__user__username=username)
	answers1 = UserInterestAnswer.objects.filter(user__username=username)
	answers = []
	for a in answers1:
		answers.append(a)
	paginator = Paginator(interests_all, 1)

	page = request.GET.get('page')
	try:
		interests = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		interests = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		interests = paginator.page(paginator.num_pages)

	return render_to_response('interests/single_user.html', locals(), context_instance=RequestContext(request))