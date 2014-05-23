from decimal import *

from django.contrib.auth.models import User


from interests.models import Interest, UserInterestAnswer
from questions.models import Question, Answer, UserAnswer, MatchAnswer

'''Compares the first UserInterstAnswer importance level to the second 
UserInterestAnswer importance level. Yes, this is a ratched way of doing it'''
def calc_interest_importance(i1, i2):
	#print i1
	if i1 == "Strongly Like":
		if i2 == "Strongly Like":
			return 100
		if i2 == "Llike":
			return 75
		if i2 == "Dislike":
			return 20
		if i2 == "Strongly Dislike":
			return 10
	elif i1 == "Like":
		if i2 == "Strongly Like":
			return 75
		if i2 == "Like":
			return 100
		if i2 == "Dislike":
			return 20
		if i2 == "Strongly Dislike":
			return 10
	elif i1 == "Dislike":
		if i2 == "Strongly Dislike":
			return 10
		if i2 == "Like":
			return 20
		if i2 == "Dislike":
			return 100
		if i2 == "Strongly Dislike":
			return 75
	elif i1 == "Strongly Dislike":
		if i2 == "Strongly Like":
			return 10
		if i2 == "Like":
			return 20
		if i2 == "Dislike":
			return 75
		if i2 == "Strongly Dislike":
			return 100
	# i1 is neutral 
	else:
		return 0


''' Calcualtes the points for the user's importance level in a specific answer
to a matched person's importance level for an answer. Also a ratched way of doing it'''
def cal_question_importance(i1, i2):
	if i1 == "Mandatory":
		if i2 == "Mandatory":
			return 100
		if i2 == "Very Important":
			return 80
		if i2 == "Somewhat Important":
			return 30
		#importance level is "not important"
		else:
			return 10
	elif i1 == "Very Important":
		if i2 == "Mandatory":
			return 90
		if i2 == "Very Important":
			return 100
		if i2 == "Somewhat Important":
			return 50
		#importance level is "not important"
		else:
			return 20
	elif i1 == "Somewhat Important":
		if i2 == "Mandatory":
			return 60
		if i2 == "Very Important":
			return 80
		if i2 == "Somewhat Important":
			return 100
		#importance level is "not important"
		else:
			return 20
	#importance level is "not important"
	else:
		if i2 == "Mandatory":
			return 20
		if i2 == "Very Important":
			return 60
		if i2 == "Somewhat Important":
			return 90
		#importance level is "not important"
		else:
			return 100



'''Calculates the points for matching users based solely off of interests
'''
def interest_points(user1, user2):
	logged_in_user_interests =  UserInterestAnswer.objects.filter(user=user1)
	viewed_user_interests =  UserInterestAnswer.objects.filter(user=user2)
	total_interests = 0
	interests_in_common = 0
	points_awarded = 0
	points_possible = 0
	for i in logged_in_user_interests:
		total_interests += 1
		for i2 in viewed_user_interests:
			#total_interests_user2 +=1
			if i.interest == i2.interest:
				interests_in_common +=1
				points_possible += 100
				print i.importance_level
				try:
					points_awarded += calc_interest_importance(i.importance_level, i2.importance_level)
				except: 
					points_awarded = 0
	if interests_in_common >= 1:
		percentage = (float(points_awarded)/float(interests_in_common)) / 100
	else: 
		percentage = 0
	print "Out %s total interests and %s interests in common, %s points were awarded of %s points with a score of %s" %(
		total_interests, interests_in_common, points_awarded, points_possible, percentage)
	return total_interests, percentage

''' Calculates the points for matching users based solely off their answers
to questions '''
def question_points(user1, user2):
	pref_answers = MatchAnswer.objects.filter(user=user1)
	actual_answers = UserAnswer.objects.filter(user=user2)
	total_questions = 0
	questions_in_common = 0
	points_awarded = 0
	points_possible = 0

	for ans in pref_answers:
		total_questions += 1 
		for act_ans in actual_answers:
			if ans.question == act_ans.question:
				questions_in_common += 1
				points_possible += 100
				if ans.answer.answer == act_ans.answer.answer:
					points_awarded += cal_question_importance(ans.importance_level, 
															act_ans.importance_level)
	if questions_in_common >= 1:
		percentage = (float(points_awarded)/float(questions_in_common)) / 100
	else: 
		percentage = 0
	print "Out of %s total questions and %s questions in common, %s points were awarded of %s points with a score of %s" %(
		total_questions, questions_in_common, points_awarded, points_possible, percentage)
	return total_questions, percentage

def match_percentage(user1, user2):
	#interest part of overall matching
	print "NEW MATCH"
	a_interests, a_i_percent = interest_points(user1, user2)
	#print "a_i_percent worked, a_i_percent is: " + str(a_i_percent)
	b_interests, b_i_percent = interest_points(user2, user1)
	#print "b_i_percent worked, b_i_percent is: " + str(b_i_percent)
	#find out largest number of liked interests between the two users. As in
	# which user liked the most interests
	if a_interests >= b_interests:
		larger_interests = a_interests
		smaller_interests = b_interests
	else:
		larger_interests = b_interests
		smaller_interests = a_interests
	#calculate ratio of smaller interests to larger
	interests_ratio = float(smaller_interests) / larger_interests
	#print "interests_ratio is: " + str(interests_ratio)

	#questions part of overall matching
	a_questions, a_q_percent = question_points(user1, user2)
	#print "a_q_percent worked, a_q_percent is: " + str(a_q_percent)
	b_questions, b_q_percent = question_points(user2, user1)
	#print "b_q_percent worked, b_q_percent is: " + str(b_q_percent)
	#find out largest number of questions answered between two users. As in 
	#which user answered the most overall questions. 
	if a_questions >= b_questions:
		larger_questions = a_questions
		smaller_questions = b_questions
	else:
		larger_questions = b_questions
		smaller_questions = a_questions
	#calculate ratio of less questions answered to more questions
	questions_ratio = float(smaller_questions) / larger_questions
	#print "questions_ratio is: " + str(questions_ratio)

	#if user1 & user2 have both answered questions and liked interests
	if a_interests >=1 and b_interests >= 1 and a_questions >=1 and b_questions >= 1:
		interest_percent = .8 * ((a_i_percent + b_i_percent) / 2) + (.2 * interests_ratio)
		question_percent = .8 * ((a_q_percent + b_q_percent) / 2) + (.2 * questions_ratio)
		percent = (interest_percent + question_percent) / 2
		overall_percent = int(percent * 100)
		print "match based on interests and questions worked, it is: " + str(overall_percent)
		return overall_percent
	# if user1 & user2 have not both answered questions, but they have
	# both liked interests
	if a_interests >=1 and b_interests >= 1 and (a_questions == 0  or b_questions == 0):
		percent = .8 * ((a_i_percent + b_i_percent) / 2) + (.2 * interests_ratio)
		interest_percent = int(percent * 100)
		print "match based on just interests worked, it is: " + str(interest_percent)
		return interest_percent
	# if user1 & user2 have not both liked interests, but have both answered
	# questions
	if (a_interests == 0 or b_interests == 0) and a_questions >= 1 and b_questions >= 1:
		percent = .8 * ((a_q_percent + b_q_percent) / 2) + (.2 * questions_ratio)
		question_percent = int(percent * 100)
		print "match based on just questions worked, it is: " + str(question_percent)
		return question_percent
	#else user1 & user2 have both not liked interests and questions
	else:
		return 0