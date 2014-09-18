# -*- coding: utf-8 -*-
import random 


from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Answer, UserAnswer
from .forms import QuestionForm, AnswerForm

def all_questions(request):
	
	questions_all = Question.objects.exclude(useranswer__user=request.user)

	paginator = Paginator(questions_all, 1)
	#importance_levels = ['Very Important', 'Somewhat Important', 'Not Important']

	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		questions = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		questions = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		question_id = request.POST['question_id']
		#print  "question importance is:" + question_id

		#user answer
		#importance_level = request.POST['importance_level']
		answer_form =  request.POST['answer']
		#answer_form = request.POST.get('answer', False)

	

		user = User.objects.get(username=request.user)
		question = Question.objects.get(id=question_id)

		#user answer save
		answer = Answer.objects.get(question=question, answer=answer_form)
		answered, created = UserAnswer.objects.get_or_create(user=user, question=question)
		answered.answer = answer
		#answered.importance_level = importance_level
		answered.save()
		questions_all = Question.objects.filter.exclude(useranswer__user=request.user)

		paginator = Paginator(questions_all, 1)
		#importance_levels = ['Very Important', 'Somewhat Important', 'Not Important']

		page = request.GET.get('page')
		try:
			questions = paginator.page(page)
		except PageNotAnInteger:
			#If page is not an integer, deliver first page.
			questions = paginator.page(1)
		except EmptyPage:
			#If page is out of range, deliver last page of results
			questions = paginator.page(paginator.num_pages)

	return render_to_response('questions/all.html', locals(), context_instance=RequestContext(request))


def edit_questions(request):
	questions_all = Question.objects.filter(useranswer__user=request.user)
	paginator = Paginator(questions_all, 1)
	importance_levels = ['Very Important', 'Somewhat Important', 'Not Important']

	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		questions = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		questions = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		question_id = request.POST['question_id']

		#user answer
		importance_level = request.POST['importance_level']
		answer_form =  request.POST['answer']
		#answer_form = request.POST.get('answer', False)


		user = User.objects.get(username=request.user)
		question = Question.objects.get(id=question_id)

		#user answer save
		answer = Answer.objects.get(question=question, answer=answer_form)
		answered, created = UserAnswer.objects.get_or_create(user=user, question=question)
		answered.answer = answer
		answered.importance_level = importance_level
		answered.save()

		return HttpResponseRedirect('')
	return render_to_response('questions/edit.html', locals(), context_instance=RequestContext(request))


def new_user_questions(request):
	
	questions_all = Question.objects.filter(for_new_users=True).exclude(useranswer__user=request.user)

	paginator = Paginator(questions_all, 1)
	#importance_levels = ['Very Important', 'Somewhat Important', 'Not Important']

	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		questions = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		questions = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		question_id = request.POST['question_id']

		#user answer
		#importance_level = request.POST['importance_level']
		answer_form =  request.POST['answer']
		#answer_form = request.POST.get('answer', False)

	

		user = User.objects.get(username=request.user)
		question = Question.objects.get(id=question_id)

		#user answer save
		answer = Answer.objects.get(question=question, answer=answer_form)
		answered, created = UserAnswer.objects.get_or_create(user=user, question=question)
		answered.answer = answer
		#answered.importance_level = importance_level
		answered.save()

		messages.success(request, 'Answer Saved')
		user_questions = UserAnswer.objects.filter(user=request.user)
		if user_questions.count() == 10: 
			return HttpResponseRedirect(reverse('handle_new_user'))
		questions_all = Question.objects.filter(for_new_users=True).exclude(useranswer__user=request.user)

		paginator = Paginator(questions_all, 1)
		#importance_levels = ['Very Important', 'Somewhat Important', 'Not Important']

		page = request.GET.get('page')
		try:
			questions = paginator.page(page)
		except PageNotAnInteger:
			#If page is not an integer, deliver first page.
			questions = paginator.page(1)
		except EmptyPage:
			#If page is out of range, deliver last page of results
			questions = paginator.page(paginator.num_pages)


	return render_to_response('questions/new_user.html', locals(), context_instance=RequestContext(request))
