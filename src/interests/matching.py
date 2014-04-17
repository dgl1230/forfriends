from decimal import *

from django.contrib.auth.models import User

from interests.models import Interest, UserInterestAnswer

def points(request_user, matched_user):
	pref_answers = MatchAnswer.objects.filter(user=request_user)
	actual_answers = UserAnswer.objects.filter(user=matched_user)
	total_questions = 0
	points_awarded = 0
	points_possible = 0

	for ans in pref_answers:
		for act_ans in actual_answers:
			if ans.question == act_ans.question:
				total_questions +=1
				points_possible += ans.points
				if ans.answer.answer == act_ans.answer.answer:
					print ans.answer
					print ans.answer.answer
					points_awarded += ans.points

	percentage = points_awarded/Decimal(points_possible)
	print "Out %s questions, %s points were awarded of %s points with a score of %s" %(
		total_questions, points_awarded, points_possible, percentage)
	return total_questions, percentage

def match_percentage(usera, userb):
	a_quests, a_percent = points(usera, userb)
	b_quests, b_percent = points(userb, usera)

	if a_quests == b_quests:
		new_percent = Decimal(a_percent * b_percent)
		n = Decimal(1.0/a_quests)
		match_percent = new_percent ** n
		print match_percent
		return match_percent