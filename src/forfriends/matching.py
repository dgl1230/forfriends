from decimal import *

from django.contrib.auth.models import User


from interests.models import Interest, UserInterestAnswer
from questions.models import Question, Answer, UserAnswer


#********** Methods used for calculating compatibility based on INTERESTS **********#
'''	Purpose:	Calculates the points for user1 and user2 for a single interest
				that they share, based on how much they like it.
	Returns:	A list with 2 attributes, the first being user1_points and the 
				second being user2_points: [user1_points, user2_points] '''
def calc_interest_importance(i1, i2):
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
    return return_tuple


'''Purpose:		Calculates the percentage compatibility between 2 users based solely
				on their interests. Uses calc_interest_importance
	Returns: 	Compatibility percentage based solely off of interest
'''
def interest_points(user1, user2):
	logged_in_user_interests = UserInterestAnswer.objects.filter(user=user1)
	viewed_user_interests = UserInterestAnswer.objects.filter(user=user2)
	interests_in_common = 0
	user1_points = 0
	user2_points = 0
	points_possible = 0
	user_score_tuple = []
	user1_interest_list = []
	user2_interest_list = []
	user1_importance_list = []
	user2_importance_list = []
	user2_temp_index = 0
	percentage = 0
	for i in logged_in_user_interests:
		user1_interest_list.append(i.interest) #list of user1's interests
		user1_importance_list.append(i.importance_level) 
	for i in viewed_user_interests:
		user2_interest_list.append(i.interest) #list of user2's interests
		user2_importance_list.append(i.importance_level)
	for i in range(len(user1_interest_list)):
		#user1 and user2 interests are shared
		if (user1_interest_list[i] in user2_interest_list):
			user2_temp_index = user2_interest_list.index(user1_interest_list[i])
			interests_in_common += 1
			points_possible += 75
			user_score_tuple = calc_interest_importance(user1_importance_list[i], user2_importance_list[user2_temp_index])
			user1_points += user_score_tuple[0]
			user2_points += user_score_tuple[1]
	if interests_in_common >= 1:
		percentage = float((points_possible - abs(user1_points - user2_points))) / float(points_possible)
	else:
		percentage = 0
	return percentage

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

'''	Purpose:	Calculates the multiplier for user1 and user2 for a single question
				that they both answered, based on how important it is to them.
	Returns:	A list with 2 attributes, the first being user1_multiplier and the 
				second being user2_multiplier: [user1_multiplier, user2_multiplier] '''
def find_importance(user1_importance, user2_importance):
	temp_list = []
	#Calculate user1's importance points
	if user1_importance == "Very Important":
		temp_list.append(2.0)
	elif user1_importance == "Somewhat Important":
		temp_list.append(1.5)
	else:
		temp_list.append(1.0)
	#Calculate user2's importance points
	if user2_importance == "Very Important":
		temp_list.append(2.0)
	elif user2_importance == "Somewhat Important":
		temp_list.append(1.5)
	else:
		temp_list.append(1.0)
	return temp_list

'''	Purpose:	Awards points to user1 and user2 based on their answers to the question
				and the multiplier of importance.
	Returns:	A list with 2 attributes, the first being user1_points and the 
				second being user2_points: [user1_points, user2_points] '''
def answer_points(user1_answer, user2_answer, importance_multiplier_list):
	temp_list = []
	user1_interest_multiplier = importance_multiplier_list[0]
	user2_interest_multiplier = importance_multiplier_list[1]
	user1_score, user2_score = 0, 0
	#Find score for user1
	if user1_answer == 1:
		user1_score = 25 * user1_interest_multiplier
	elif user1_answer == 2:
		user1_score = 15 * user1_interest_multiplier
	elif user1_answer == 3:
		user1_score = 0 * user1_interest_multiplier
	elif user1_answer == 4:
		user1_score = -15 * user1_interest_multiplier
	else:
		user1_score = -25 * user1_interest_multiplier

	#Find score for user2
	if user2_answer == 1:
		user2_score = 25 * user2_interest_multiplier
	elif user2_answer == 2:
		user2_score = 15 * user2_interest_multiplier
	elif user2_answer == 3:
		user2_score = 0 * user2_interest_multiplier
	elif user2_answer == 4:
		user2_score = -15 * user2_interest_multiplier
	else:
		user2_score = -25 * user2_interest_multiplier
	temp_list.append(user1_score)
	temp_list.append(user2_score)
	return temp_list

'''	Purpose:	Awards points to user1 and user2 based on their answers to the question
				and the multiplier of importance.
	Returns:	A list with 2 attributes, the first being user1_points and the 
				second being user2_points: [user1_points, user2_points] '''
def question_points(user1, user2):
	user1_answers = UserAnswer.objects.filter(user=user1)
	user2_answers = UserAnswer.objects.filter(user=user2)
	points_possible = 0
	user1_points = 0
	user2_points = 0
	questions_in_common = 0
	percentage = 0
	user2_index = 0
	user1_question_list = []
	user1_importance_list = []
	user1_answer_list = []
	user2_question_list = []
	user2_importance_list = []
	user2_answer_list = []
	for ans in user1_answers:
		user1_question_list.append(ans.question)
		user1_importance_list.append(ans.importance_level)
		user1_answer_list.append(ans.answer.pattern_number)
	for ans in user2_answers:
		user2_question_list.append(ans.question)
		user2_importance_list.append(ans.importance_level)
		user2_answer_list.append(ans.answer.pattern_number)
	for i in range(len(user1_question_list)):
		if user1_question_list[i] in user2_question_list:
			#index for user2's question, answer, importance, and pattern
			user2_index = user2_question_list.index(user1_question_list[i])
			questions_in_common += 1
			points_possible += 100
			user_list = []
			importance_list = []
			importance_list = find_importance(user1_importance_list[i], user2_importance_list[user2_index])
			user_list = answer_points(user1_answer_list[i], user2_answer_list[user2_index], importance_list)
			user1_points += user_list[0]
			user2_points += user_list[1]
	if points_possible >= 100:
		percentage = (points_possible - abs(user1_points - user2_points)) / points_possible
	else:
		percentage = 0
	return percentage

def match_percentage(user1, user2):
	overall_score = 0.0
	question_score = question_points(user1, user2) #question compatibility score
	interest_score = interest_points(user1, user2) #interest compatibility score
	if(interest_score == 0 and question_score == 0):
		overall_score = 0
	elif(interest_score == 0):
		overall_score = question_score
	elif(question_score == 0):
		overall_score = interest_score
	else:
		overall_score = (.8 * question_score) + (.2 * interest_score)
	return int(round(overall_score * 100))