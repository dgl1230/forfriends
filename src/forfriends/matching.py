from decimal import *
from datetime import date, datetime, timedelta
import logging

from django.contrib.auth.models import User


from interests.models import Interest, UserInterestAnswer
from questions.models import Question, Answer, UserAnswer

#We don't need this as much"
#********** Methods used for calculating compatibility based on INTERESTS **********#
'''	Purpose:	Calculates the points for user1 and user2 for a single interest
				that they share, based on how much they like it.
	Returns:	A list with 2 attributes, the first being user1_points and the 
				second being user2_points: [user1_points, user2_points] '''
'''def calc_interest_importance(i1, i2):
	user1_points = 50 #start with bases of 50
	user2_points = 50
	return_tuple = []
	#Calculate points for user1
	if i1 == "Strongly Like":
		user1_points = 75
	elif i1 == "Like":
		user1_points = 65
	elif i1 == "Neutral":
		user1_points = 50
	elif i1 == "Dislike":
		user1_points = 35
	elif i1 == "Strongly Dislike":
		user1_points = 25
	    
	#Calculate points for user2
	if i2 == "Strongly Like":
		user2_points = 75
	elif i2 == "Like":
		user2_points = 65
	elif i2 == "Neutral":
		user2_points = 50
	elif i2 == "Dislike":
		user2_points = 35
	elif i2 == "Strongly Dislike":
		user2_points = 25
	return_tuple.append(user1_points)
	return_tuple.append(user2_points)
	return return_tuple'''


#Returns a tuple, where the first element is the # of categories shared and the second
#element is the number of interests shared
def interest_points(user1, user2):
	start_time = datetime.now()
	logged_in_user_interests = UserInterestAnswer.objects.filter(user=user1)
	viewed_user_interests = UserInterestAnswer.objects.filter(user=user2)
	categories_shared = 0
	interests_shared = 0
	user1_list = []
	user1_interest_list = []
	user2_dict = {}
	user2_interest_dict = {}
	category_count1 = 0
	category_count2 = 0
	#could move this for loop into range(len(user1_list)) possibly
	for i in logged_in_user_interests:
		user1_list.append(i.interest.category)
		user1_interest_list.append(i.interest)
		category_count1 = category_count1 + 1
	for i in viewed_user_interests:
		user2_dict[i.interest.category] = i.interest
		user2_interest_dict[i.interest] = "x"
		category_count2 = category_count2 + 1
	for i in range(len(user1_list)):
		user1_category = user1_list[i]
		if user1_category in user2_dict:
			categories_shared = categories_shared + 1
	if categories_shared != 0:
		for i in range(len(user1_interest_list)):
			user1_interest = user1_interest_list[i]
			if user1_interest in user2_interest_dict:
				interests_shared = interests_shared + 1
	total_categories = category_count1 + category_count2
	return_tuple = (categories_shared, interests_shared, total_categories)
	end_time = datetime.now()
	logging.debug("Interest_points time is: " + str(end_time - start_time))
	return return_tuple

# Method that returns a list of shared interests between two users
def find_same_interests(user1, user2):
	start_time = datetime.now()
	logged_in_user_interests = UserInterestAnswer.objects.filter(user=user1)
	viewed_user_interests = UserInterestAnswer.objects.filter(user=user2)
	number_in_common = 0
	user1_list = []
	user2_dict = {}
	common_interest_list = []
	for i in logged_in_user_interests:
		user1_list.append(i.interest)
	for i in viewed_user_interests:
		user2_dict[i.interest] = "irrelephant"
	for i in range(len(user1_list)):
		user1_interest = user1_list[i]
		user2_interest = user2_dict.pop(user1_interest, "false")
		if user2_interest != "false":
			common_interest_list.append(user1_interest)
			number_in_common = number_in_common + 1
	end_time = datetime.now()
	logging.debug("Dictionary time is: " + str(end_time - start_time))
	return common_interest_list


#********** Methods used for calculating compatibility based on QUESTIONS **********#
""" 
	Answer Types:
		1. Extreme Positive, 2. Positive, 3. Neutral, 4. Negative, 5. Extreme Negative
	Question Types:
		1: 1, 2, 3, 4, 5
		2: 1, 2, 4, 5
		3: 1, 3, 5
		4: 1, 5
	Interest Types:
		1. Very Interested
		2. Somewhat Interested
		3. Not Interested
"""

'''	Purpose:	Awards points to user1 and user2 based on their answers to the question
				and the multiplier of importance.
	Returns:	A list with 2 attributes, the first being user1_points and the 
				second being user2_points: [user1_points, user2_points] '''
def answer_points(user1_answer, user2_answer, weight):
	temp_list = []
	user1_score, user2_score = 0, 0
	#Find score for user1
	if user1_answer == 1:
		user1_score = 25  * weight
	else:
		user1_score = -25  * weight

	#Find score for user2
	if user2_answer == 1:
		user2_score = 25 * weight
	else:
		user2_score = -25 * weight

	temp_list.append(user1_score)
	temp_list.append(user2_score)
	return temp_list

'''	Purpose:	Awards points to user1 and user2 based on their answers to the question
				and the multiplier of importance.
	Returns:	A list with 2 attributes, the first being user1_points and the 
				second being user2_points: [user1_points, user2_points] '''
def question_points(user1, user2):
	start_time = datetime.now()
	user1_answers = UserAnswer.objects.filter(user=user1)
	user2_answers = UserAnswer.objects.filter(user=user2)
	points_possible = 0
	user1_points = 0
	user2_points = 0
	percentage = 0
	user1_list = []
	user2_dict = {}
	for ans in user1_answers:
		user1_list.append([ans.question, ans.question.weight, ans.answer.value])
	for ans in user2_answers:
		user2_dict[ans.question] = ans.answer.value
	for i in range(len(user1_list)):
		user1_question = user1_list[i][0]
		importance_multiplier = user1_list[i][1]
		user1_answer = user1_list[i][2]
		user2_answer = user2_dict.pop(user1_question, "false")
		if user2_answer != "false":
			points_possible += 100
			user_list = []
			user_list = answer_points(user1_answer, user2_answer, importance_multiplier)
			user1_points += user_list[0]
			user2_points += user_list[1]
	if points_possible >= 100:
		percentage = (points_possible - abs(user1_points - user2_points)) * 100 / points_possible
	else:
		percentage = 0
	end_time = datetime.now()
	logging.debug("Question_Points time is: " + str(end_time - start_time))
	logging.debug("HEY, SHOW UP")
	return percentage

def match_percentage(user1, user2):
	start_time = datetime.now()
	overall_score = 0.0
	question_score = int(round(question_points(user1, user2))) #question compatibility score
	score_difference = 100 - question_score
	multiplier = 0.0

	#number of shared categories, and number of shared interests
	interest_tuple = interest_points(user1, user2) 
	shared_categories = interest_tuple[0]
	shared_interests = interest_tuple[1]
	total_categories = interest_tuple[2]
	if (shared_interests != 0):
		multiplier = float(shared_interests) / float(shared_categories)
	else:
		multiplier = float(shared_categories) / float(total_categories)
	interest_score = multiplier * score_difference
	
	
	overall_score = int(round(question_score + interest_score))
	end_time = datetime.now()
	logging.debug("Match percentage time is: " + str(end_time - start_time))
	logging.debug("Overall match percentage is: " + str(int(round(overall_score))))
	return overall_score