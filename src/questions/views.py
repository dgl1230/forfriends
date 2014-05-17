from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Answer, UserAnswer, MatchAnswer
from .forms import QuestionForm, AnswerForm


def all_questions(request):
	questions_all = Question.objects.all()
	paginator = Paginator(questions_all, 1)
	importance_levels = ['Mandatatory', 'Very Important', 'Somewhat Important', 'Not Important']

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

		#user match answer
		match_importance_level = request.POST['match_importance_level']
		match_answer_form = request.POST['match_answer']
		#match_answer_form = request.POST.get('match_answer', False)

		user = User.objects.get(username=request.user)
		question = Question.objects.get(id=question_id)

		#user answer save
		answer = Answer.objects.get(question=question, answer=answer_form)
		answered, created = UserAnswer.objects.get_or_create(user=user, question=question)
		answered.answer = answer
		answered.importance_level = importance_level
		points = assign_points(importance_level)
		answered.points = points
		answered.save()

		#user match answer save
		user_answer = Answer.objects.get(question=question, answer=match_answer_form)
		answered, created = MatchAnswer.objects.get_or_create(user=user, question=question)
		answered.answer = user_answer
		answered.importance_level = match_importance_level
		points = assign_points(match_importance_level)
		answered.points = points
		answered.save()

		messages.success(request, 'Answer Saved')
	return render_to_response('questions/all.html', locals(), context_instance=RequestContext(request))



def create_question(request):
	q_form = QuestionForm(request.POST or None)
	a_form = AnswerForm(request.POST or None)
	if q_form.is_valid():
		if a_form.is_valid():
			question = q_form.save(commit=False)
			answer = a_form.save(commit=False)
			question.user = request.user
			question.save()
			answer.question = question
			answer.save()
			messages.success(request, 'Question Created')
			return HttpResponseRedirect('/')

	return render_to_response("questions/create.html", locals(),
		 context_instance=RequestContext(request))

