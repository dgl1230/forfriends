# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from .models import Interest, UserInterestAnswer, Category
from .forms import InterestForm
from django.core.urlresolvers import reverse
from django.core.cache import cache
from profiles.views import user_not_new


@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def all_interests(request):
	user_interests = Interest.objects.filter(userinterestanswer__user=request.user)
	video_games = Interest.objects.filter(category__title='Video/Computer Games')
	card_games = Interest.objects.filter(category__title='Card Games')
	board_games = Interest.objects.filter(category__title='Board Games')
	dancing = Interest.objects.filter(category__title='Dancing')
	musical_instruments = Interest.objects.filter(category__title='Musical Instruments')
	games = Interest.objects.filter(category__title='Games')
	fitness_sports = Interest.objects.filter(category__title='Fitness/Sports')
	extreme_sports = Interest.objects.filter(category__title='Extreme Sports')
	combat_sports = Interest.objects.filter(category__title='Combat Sports')
	team_sports = Interest.objects.filter(category__title='Team Sports')
	outdoor_activities = Interest.objects.filter(category__title='Outdoor Activities')
	performing_arts = Interest.objects.filter(category__title='Performing Arts and Music')
	dancing = Interest.objects.filter(category__title='Dancing')
	arts_crafts = Interest.objects.filter(category__title='Arts and Crafts')
	spiritual = Interest.objects.filter(category__title='Spirituality')
	food = Interest.objects.filter(category__title='Food/Cooking')
	news = Interest.objects.filter(category__title='News/Current Events')
	indoor = Interest.objects.filter(category__title='Indoor Activities')
	
	return render_to_response('interests/experimental.html', locals(), context_instance=RequestContext(request))


def save_interest(request, interest_id):
	interest = Interest.objects.get(id=interest_id)
	num_of_interests = Interest.objects.filter(userinterestanswer__user=request.user).count()
	try: 
		answered = UserInterestAnswer.objects.get(user=request.user, interest=interest)
		answered.delete()
	except: 
		if num_of_interests >= 10:
			return HttpResponseRedirect(reverse('interests'))
		answered = UserInterestAnswer.objects.create(user=request.user, interest=interest)
		answered.save()
	return HttpResponseRedirect(reverse('interests'))



@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def create_interest(request):
	form = InterestForm(request.POST or None)
	if form.is_valid():
		interest = form.save(commit=False)
		interest.save()
		messages.success(request, 'Thanks for contributing to Frenvu! Once we look over your interest, other users will be able to like it!')
		return HttpResponseRedirect(reverse('create'))


	return render_to_response("interests/create.html", locals(), context_instance=RequestContext(request))

''''
@user_passes_test(user_not_new, login_url=reverse_lazy('new_user_info'))
def all_interests(request):
	
	#interests_all = Interest.objects.exclude(userinterestanswer__user=request.user).filter(approved=True).order_by('?')
	
	if not request.session.get('random_interests'):
		request.session['random_interests']= request.user.id
	interests_all = cache.get('random_interests_%d' % request.session['random_interests'])
	if not interests_all:
		interests_all = list(Interest.objects.exclude(userinterestanswer__user=request.user).filter(approved=True).order_by('?'))
		cache.set('random_interests_%d' % request.session['random_interests'], interests_all, 100)

	paginator = Paginator(interests_all, 1)
	importance_levels = ['Strongly Dislike', 'Dislike', 'Neutral', 'Like', 'Strongly Like']

	page = request.GET.get('page')
	try:
		interests = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		interests = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		interests = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		interest_id = request.POST['interest_id']

		#user answer
		try:
			importance_level = request.POST['importance_level']
		except: 
			messages.error(request, "Please select an importance level first")
			HttpResponseRedirect(reverse('home'))

		user = User.objects.get(id=request.user.id)
		interest = Interest.objects.get(id=interest_id)
		try:
			interest_pic = InterestPicture.objects.get(interest=interest).filter(id=1)
		except: 
			pass

		#user answer save

		answered, created = UserInterestAnswer.objects.get_or_create(user=user, interest=interest)
		answered.importance_level = importance_level
		answered.save()
		if not request.session.get('random_interests'):
			request.session['random_interests']= request.user.id
		interests_all = list(Interest.objects.exclude(userinterestanswer__user=request.user).filter(approved=True).order_by('?'))
		cache.set('random_interests_%d' % request.session['random_interests'], interests_all, 100)
		paginator = Paginator(interests_all, 1)
		importance_levels = ['Strongly Dislike', 'Dislike', 'Neutral', 'Like', 'Strongly Like']

		page = request.GET.get('page')
	
		try:
			interests = paginator.page(page)
		except PageNotAnInteger:
		#If page is not an integer, deliver first page.
			interests = paginator.page(1)
		except EmptyPage:
		#If page is out of range, deliver last page of results
			interests = paginator.page(paginator.num_pages)


	return render_to_response('interests/all.html', locals(), context_instance=RequestContext(request))
'''



@user_passes_test(user_not_new)
def search_interests(request):
	try:
		q = request.GET.get('q', '')
	except: 
		q = False
	interest_queryset = Interest.objects.filter(interest__icontains=q)
	results = interest_queryset
	return render_to_response('interests/search.html', locals(), context_instance=RequestContext(request))


