from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Interest, UserInterestAnswer, InterestPicture
from .forms import InterestForm


"""Function for converting string representing importance level in the paginators
to the UserInterestAnswer model's choice field
"""
def convert_to_model_importance(il):
	if il == "Strongly Like":
		return "SL"
	if il == "Like":
		return "L"
	if il == "Dislike":
		return "DL"
	if il == "Strongly Dislike":
		return "SD"
	else:
		return "N"


def create_interest(request):
	form = InterestForm(request.POST or None)
	if form.is_valid():
		interest = form.save(commit=False)
		interest.user = request.user
		interest.save()
		messages.success(request, 'Interest Created')
		return HttpResponseRedirect('/')

	return render_to_response("interests/create.html", locals(),
		 context_instance=RequestContext(request))


def all_interests(request):
	interests_all = Interest.objects.exclude(userinterestanswer__isnull=False)
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
		answered.importance_level = convert_to_model_importance(importance_level)
		answered.save()

		messages.success(request, 'Answer Saved')
	return render_to_response('interests/all.html', locals(), context_instance=RequestContext(request))


def edit_interests(request):
	interests_all = Interest.objects.exclude(userinterestanswer__isnull=True)
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
		answered.importance_level = convert_to_model_importance(importance_level)
		answered.save()

		messages.success(request, 'Changes Saved')
		return HttpResponseRedirect('')
	return render_to_response('interests/edit.html', locals(), context_instance=RequestContext(request))

